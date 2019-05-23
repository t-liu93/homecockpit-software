import struct
from network import datatypes
"""
This class is used to handle data types,
i.e. convert socket data into datatype used by this application,
and vice versa
network is also implemented here
"""
class DataHandler():
    def __init__(self):
        self.__data = None
        self.__type = None

    @property
    def Data(self):
        return self.__data
    
    @Data.setter
    def Data(self, databyte):
        self.__data = databyte

    @property
    def Type(self):
        return self.__type

    @Type.setter
    def Type(self, t):
        self.__type = t

    def Decode(self, customData):
        msg = struct.unpack_from("=4scf500s", self.__data) # at this moment DREF should be unpacked as this type
        value = msg[2]
        remaining = msg[3]
        self.__type = self.__RemoveZeros(msg[3])

        customData.Value = value
        customData.Name = self.__type

        return customData
    
    def __RemoveZeros(self, dataRemaining):
        i = 0
        for b in dataRemaining:
            if not b == 0:
                i += 1
        return dataRemaining[0:i].decode("ASCII")

