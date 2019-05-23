"""
Data reference data defines
"""
class DataReference():
    def __init__(self, value, name):
        self.__value = value # value of dataref is float
        self.__name = name # name will be a string


    """
    Generic defines of message length,
    for datareference, the message type is 509
    """
    @property
    def MsgLength(self):
        return 509

    """
    values in float of the message
    each data reference should only contains one value
    """
    @property
    def Value(self):
        return self.__value

    @Value.setter
    def Value(self, value):
        self.__value = value

    """
    Name of this reference for better understanding
    """
    @property
    def Name(self):
        return self.__name

    @Name.setter
    def Name(self, name):
        self.__name = name    