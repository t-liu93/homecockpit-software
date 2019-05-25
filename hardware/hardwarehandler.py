import collections
import threading
import time
import RPi.GPIO as GPIO  # pylint: disable=import-error
from hardware.charlcd import characterlcd

BUTTON_GPIO             = 18
ENCODER_COARSE_CLK_GPIO = 12
ENCODER_COARSE_DT_GPIO  = 16
ENCODER_FINE_CLK_GPIO   = 20
ENCODER_FINE_DT_GPIO    = 21

BOUNCE_TIME_BUTTON      = 200
BOUNCE_TIME_ENCODER     = 100

LCD_REFRESH_INTERVAL    = 0.5

"""
Class to control the radio panel
Currently only com1 can be controled
"""
class RadioPanel(threading.Thread):
    def __init__(self, queue, name):
        threading.Thread.__init__(self)
        self.__queue = queue
        self.__name = name
        self.__com1Freq = {'actv' : 0.0, 'stby' : 0.0}
        self.__textArray = list()
        self.__textArray.append("")
        self.__textArray.append("")

        self.__lastRefreshTime = time.time()

        self.__coarseClk = 0
        self.__coarseDt = 0
        self.__fineClk = 0
        self.__fineDt = 0

        self.__panelLcd = characterlcd.CharacterLCD('PCF8574', 1, 0x27, 16, 2)

        """
        setting up GPIO
        """
        GPIO.setmode(GPIO.BCM)
        """
        I use my connection here, here button connect to GPIO18
        Encoder1 connect to GPIO12 and GPIO16
        Encoder2 connect to GPIO20 and GPIO21
        """
        GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(ENCODER_COARSE_CLK_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(ENCODER_COARSE_DT_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(ENCODER_FINE_CLK_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(ENCODER_FINE_DT_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        """
        Event detection when thread starts
        """
        GPIO.add_event_detect(
            BUTTON_GPIO, GPIO.FALLING, callback=self.__SwitchFreq, bouncetime=BOUNCE_TIME_BUTTON)
        """
        Clockwise: dt -> clk
        Anti-clockwise: clk -> dt
        """
        GPIO.add_event_detect(ENCODER_COARSE_CLK_GPIO, GPIO.FALLING,
                              callback=self.__CoarseUp, bouncetime=BOUNCE_TIME_ENCODER)
        GPIO.add_event_detect(ENCODER_COARSE_DT_GPIO, GPIO.FALLING,
                              callback=self.__CoarseDown, bouncetime=BOUNCE_TIME_ENCODER)
        GPIO.add_event_detect(ENCODER_FINE_CLK_GPIO, GPIO.FALLING,
                              callback=self.__FineUp, bouncetime=BOUNCE_TIME_ENCODER)
        GPIO.add_event_detect(ENCODER_FINE_DT_GPIO, GPIO.FALLING,
                              callback=self.__FineDown, bouncetime=BOUNCE_TIME_ENCODER)
        # TODO: at this moment is not as stable as I expected, so it will be modified later.
    
    def run(self):
        while True:
            if (not self.__queue.networktohardware.empty()):
                radioFreq = self.__queue.networktohardware.get()
                if radioFreq.Name == "com1actv":
                    # print("should be com1Actv, ", radioFreq.Value)
                    self.__com1Freq['actv'] = float(radioFreq.Value) / 100
                elif radioFreq.Name == "com1stby":
                    # print("should be com1Stby, ", radioFreq.Value)
                    self.__com1Freq['stby'] = float(radioFreq.Value) / 100
                elif radioFreq.Name == "com2actv":
                    # print("should be com2Actv, ", radioFreq.Value)
                    pass
                elif radioFreq.Name == "com2stby":
                    # print("should be com2Stby, ", radioFreq.Value)
                    pass

            if time.time() - self.__lastRefreshTime > LCD_REFRESH_INTERVAL:
                # self.__textArray[0] = "ACTV: " + str(self.__com1Freq['actv'])
                # self.__textArray[1] = "STBY: " + str(self.__com1Freq['stby'])
                # self.__panelLcd.Write(self.__textArray, len(self.__textArray))
                self.__panelLcd.WriteString("ACTV: " + str(self.__com1Freq['actv']) + "\n\r" 
                    + "STBY: " + str(self.__com1Freq['stby']))
                self.__lastRefreshTime = time.time()

    def __SwitchFreq(self, gpioPin):
        

    def __CoarseUp(self, gpioPin):
        self.__coarseClk += 1
        if GPIO.input(ENCODER_COARSE_DT_GPIO) == False and self.__coarseDt == 1:
            print("coarseup")
        self.__coarseClk = 0
        self.__coarseDt = 0


    def __CoarseDown(self, gpioPin):
        self.__coarseDt += 1
        if GPIO.input(ENCODER_COARSE_CLK_GPIO) == False and self.__coarseClk == 1:
            print("coarsedown")
        self.__coarseDt = 0
        self.__coarseClk = 0

    def __FineUp(self, gpioPin):
        if GPIO.input(ENCODER_FINE_DT_GPIO) == False:
            print("fineup")

    def __FineDown(self, gpioPin):
        if GPIO.input(ENCODER_FINE_CLK_GPIO) == False:
            print("finedown")
