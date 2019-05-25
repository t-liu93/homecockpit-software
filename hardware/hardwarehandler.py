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
BOUNCE_TIME_ENCODER     = 150

LCD_REFRESH_INTERVAL    = 0.2

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

        self.__toRefresh = True

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
                              callback=self.__CoarseChange, bouncetime=BOUNCE_TIME_ENCODER)
        # GPIO.add_event_detect(ENCODER_COARSE_DT_GPIO, GPIO.FALLING,
                            #   callback=self.__CoarseDown, bouncetime=BOUNCE_TIME_ENCODER)
        GPIO.add_event_detect(ENCODER_FINE_CLK_GPIO, GPIO.FALLING,
                              callback=self.__FineChange, bouncetime=BOUNCE_TIME_ENCODER)
        # GPIO.add_event_detect(ENCODER_FINE_DT_GPIO, GPIO.FALLING,
                            #   callback=self.__FineDown, bouncetime=BOUNCE_TIME_ENCODER)
        # TODO: at this moment is not as stable as I expected, so it will be modified later.
    
    def run(self):
        while True:
            if (not self.__queue.networktohardware.empty()):
                radioFreq = self.__queue.networktohardware.get()
                if radioFreq.Name == "com1actv":
                    if radioFreq.Value / 100 != self.__com1Freq['actv']:
                        self.__com1Freq['actv'] = radioFreq.Value / 100
                        self.__toRefresh = True
                elif radioFreq.Name == "com1stby":
                    if radioFreq.Value / 100 != self.__com1Freq['stby']:
                        self.__com1Freq['stby'] = radioFreq.Value / 100
                        self.__toRefresh = True

            if time.time() - self.__lastRefreshTime > LCD_REFRESH_INTERVAL and self.__toRefresh:
                self.__toRefresh = False
                self.__panelLcd.WriteString("ACTV: " + str(self.__com1Freq['actv'])
                                            + "\n\r" + "STBY: " + str(self.__com1Freq['stby']))
                self.__lastRefreshTime = time.time()

    def __SwitchFreq(self, gpioPin):
        # swap the stby and actv
        self.__queue.hardwaretonetwork.put(["com1actv", self.__com1Freq['stby']])
        self.__queue.hardwaretonetwork.put(["com1stby", self.__com1Freq['actv']])

    def __CoarseChange(self, gpioPin):
        if GPIO.input(ENCODER_COARSE_DT_GPIO) == False:
            self.__GetNextCoarse(True)
        else:
            self.__GetNextCoarse(False)

    def __FineChange(self, gpioPin):
        if GPIO.input(ENCODER_FINE_DT_GPIO) == False:
            self.__GetNextFine(True)
        else:
            self.__GetNextFine(False)

    def __GetNextCoarse(self, plus):
        newFreq = 0
        if plus:
            newFreq = self.__com1Freq['stby'] + 1
            if newFreq > 136.99:
                newFreq = 118.0 + (newFreq * 100 % 100 / 100)
        else:
            newFreq = self.__com1Freq['stby'] - 1
            if newFreq < 118.00:
                newFreq = 136.00 + (newFreq * 100 % 100 / 100)
        self.__queue.hardwaretonetwork.put(["com1stby", newFreq])
    
    # TODO: add 8.33Khz supporting
    def __GetNextFine(self, plus):
        newFreq = 0
        if plus:
            newFreq = self.__com1Freq['stby'] + 0.01
            if newFreq * 100 % 100 > 99:
                newFreq = divmod(newFreq, 1)[1]
        else:
            newFreq = self.__com1Freq['stby'] - 0.01
            if newFreq * 100 % 100 < 0:
                newFreq = divmod(newFreq, 1)[1] + 0.99
        self.__queue.hardwaretonetwork.put(
            ["com1stby", newFreq])
