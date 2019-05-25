from network import datatypes
import socket
import struct
import threading
import time


"""
This class is used to handle data types,
i.e. convert socket data into datatype used by this application,
and vice versa
network is also implemented here
"""
class DataHandler(threading.Thread):
    def __init__(self, radioQueue, name, receivingPort, sendingPort):
        threading.Thread.__init__(self)
        # use queue to pass data from network to hardware
        self.__radioQueue = radioQueue
        # network attributes, shall be read from argument
        self.__name = name
        self.__receivingPort = receivingPort
        self.__sendingPort = sendingPort

        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__sock.bind(("", self.__receivingPort))

        # following the data maintained by the data handler
        self.__com1Actv = datatypes.DataReference()
        self.__com1Stby = datatypes.DataReference()
        self.__com2Actv = datatypes.DataReference()
        self.__com2Stby = datatypes.DataReference()


    def run(self):
        while True:
            self.__data, self.__address = self.__sock.recvfrom(509) # At this moment 509 is enough for data ref
            self.Decode()


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

    """
    Used to decode message from socket, and convert it into usable data
    """
    def Decode(self):
        msg = struct.unpack_from("=4scf500s", self.__data) # at this moment DREF should be unpacked as this type
        refName = self.__RemoveZeros(msg[3])
        if refName == "sim/cockpit/radios/com1_freq_hz":
            self.__com1Actv.Value = msg[2]
            self.__com1Actv.Name = self.__GetDataType(refName)
            self.__PutInQueue(self.__com1Actv)
        elif refName == "sim/cockpit/radios/com1_stdby_freq_hz":
            self.__com1Stby.Value = msg[2]
            self.__com1Stby.Name = self.__GetDataType(refName)
            self.__PutInQueue(self.__com1Stby)
        elif refName == "sim/cockpit/radios/com2_freq_hz":
            self.__com2Actv.Value = msg[2]
            self.__com2Actv.Name = self.__GetDataType(refName)
            self.__PutInQueue(self.__com2Actv)
        elif refName == "sim/cockpit/radios/com2_stdby_freq_hz":
            self.__com2Stby.Value = msg[2]
            self.__com2Stby.Name = self.__GetDataType(refName)
            self.__PutInQueue(self.__com2Stby)
    
    def __RemoveZeros(self, dataRemaining):
        i = 0
        for b in dataRemaining:
            if not b == 0:
                i += 1
        return dataRemaining[0:i].decode("ASCII")

    def __GetDataType(self, typeStr):
        return {
            "sim/cockpit/radios/com1_freq_hz" : "com1actv",
            "sim/cockpit/radios/com1_stdby_freq_hz" : "com1stby",
            "sim/cockpit/radios/com2_freq_hz" : "com2actv",
            "sim/cockpit/radios/com2_stdby_freq_hz" : "com2stby"
        }[typeStr]

    def __PutInQueue(self, newValue):
        if not self.__radioQueue.networktohardware.full():
            self.__radioQueue.networktohardware.put(newValue)
