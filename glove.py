from ctypes import *
from enum import IntEnum

FDGLOVE_DLL = cdll.LoadLibrary("fglove64")

class GloveType(IntEnum):
    GLOVENONE = 0
    GLOVE5U = 1	
    GLOVE5UW = 2	
    GLOVE5U_USB = 3
    GLOVE7 = 4     
    GLOVE7W = 5    
    GLOVE16 = 6    
    GLOVE16W = 7   
    GLOVE14U = 8	
    GLOVE14UW = 9	
    GLOVE14U_USB = 10

class GloveHand(IntEnum):
    HAND_LEFT = 0
    HAND_RIGHT = 1

class SensorTypes(IntEnum):
    THUMBNEAR = 0
    THUMBFAR = 1
    THUMBINDEX = 2
    INDEXNEAR = 3
    INDEXFAR = 4
    INDEXMIDDLE = 5
    MIDDLENEAR = 6
    MIDDLEFAR = 7
    MIDDLERING = 8
    RINGNEAR = 9
    RINGFAR = 10
    RINGLITTLE = 11
    LITTLENEAR = 12
    LITTLEFAR = 13
    THUMBPALM = 14
    WRISTBEND = 15
    PITCH = 16
    ROLL = 17

class FDGlove():
    def __init__(self, port):
        port = c_char_p(port.encode("utf-8"))

        fdOpen = FDGLOVE_DLL.fdOpen
        fdOpen.restype = c_void_p
        fdOpen.argtypes = [c_char_p]

        self.glove = fdOpen(port)
        self.glove = c_void_p(self.glove)
        if self.glove == 0:
            raise IOError("Could not connect to 5DT glove.")            

        # Setup function prototypes
        self.fdGetSensorRaw = FDGLOVE_DLL.fdGetSensorRaw
        self.fdGetSensorRaw.restype = c_ushort
        self.fdGetSensorRaw.argtype = [c_void_p, c_int]

        self.fdGetSensorRawAll = FDGLOVE_DLL.fdGetSensorRawAll
        self.fdGetSensorRawAll.restype = None
        self.fdGetSensorRawAll.argtype = [c_void_p, c_void_p]

        self.fdGetSensorScaled = FDGLOVE_DLL.fdGetSensorScaled
        self.fdGetSensorScaled.restype = c_float
        self.fdGetSensorScaled.argtype = [c_void_p, c_int]

        self.fdGetSensorScaledAll = FDGLOVE_DLL.fdGetSensorScaledAll
        self.fdGetSensorScaledAll.restype = None
        self.fdGetSensorScaledAll.argtype = [c_void_p, c_void_p]

    def __enter__(self):
        return self
    
    def __exit__(self, exception_type, exception_value, traceback):
        self.close()

    def get_sensor_raw(self, n_sensor):
        sensor_val = c_int(n_sensor)
        return self.fdGetSensorRaw(self.glove, sensor_val)

    def get_sensor_raw_all(self):
        p_data = (c_ushort * 20)()
        self.fdGetSensorRawAll(self.glove, p_data)
        return list(p_data)

    def get_sensor_scaled(self, n_sensor):
        sensor_val = c_int(n_sensor)
        return self.fdGetSensorScaled(self.glove, sensor_val)

    def get_sensor_scaled_all(self):
        p_data = (c_float * 20)()
        self.fdGetSensorScaledAll(self.glove, p_data)
        return list(p_data)
           
    def close(self):
        fdClose = FDGLOVE_DLL.fdClose
        fdClose.argtypes = [c_void_p]
        fdClose.restype = c_int
        
        return fdClose(self.glove)

def fd_glove_open(port):
    return FDGlove(port)
   
if __name__ == "__main__":
    with fd_glove_open("usb0") as glove:
        while True:
            sensor_val = glove.get_sensor_scaled(0)
            print(sensor_val)
