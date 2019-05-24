import threading
import time

class RadioPanel(threading.Thread):
    def __init__(self, queue, name):
        threading.Thread.__init__(self)
        self.__queue = queue
        self.__name = name
    
    def run(self):
        while True:
            radioFreq = self.__queue.get()
            if radioFreq.Name == "com1actv":
                print("should be com1Actv, ", radioFreq.Value)
            elif radioFreq.Name == "com1stby":
                print("should be com1Stby, ", radioFreq.Value)
            elif radioFreq.Name == "com2actv":
                print("should be com2Actv, ", radioFreq.Value)
            elif radioFreq.Name == "com2stby":
                print("should be com2Stby, ", radioFreq.Value)