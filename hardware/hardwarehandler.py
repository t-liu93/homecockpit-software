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
BOUNCE_TIME_ENCODER     = 50

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
        GPIO.setup(ENCODER_COARSE_CLK_GPIO, GPIO.IN)
        GPIO.setup(ENCODER_COARSE_DT_GPIO, GPIO.IN)
        GPIO.setup(ENCODER_FINE_CLK_GPIO, GPIO.IN)
        GPIO.setup(ENCODER_FINE_DT_GPIO, GPIO.IN)

        self.__coarseCLKCounter = 0
        self.__coarseDTCounter = 0
        self.__fineCLKCounter = 0
        self.__fineDTCounter = 0

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
                              callback=self.__CoarseCLKChange, bouncetime=BOUNCE_TIME_ENCODER)
        GPIO.add_event_detect(ENCODER_COARSE_DT_GPIO, GPIO.FALLING,
                              callback=self.__CoarseDTChange, bouncetime=BOUNCE_TIME_ENCODER)
        GPIO.add_event_detect(ENCODER_FINE_CLK_GPIO, GPIO.FALLING,
                              callback=self.__FineCLKChange, bouncetime=BOUNCE_TIME_ENCODER)
        GPIO.add_event_detect(ENCODER_FINE_DT_GPIO, GPIO.FALLING,
                              callback=self.__FineDTChange, bouncetime=BOUNCE_TIME_ENCODER)
    
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
                self.__panelLcd.WriteString("ACTV: " + "{:5.2f}".format(self.__com1Freq['actv']) + "MHz"
                                            + "\n\r" + "STBY: " + "{:5.2f}".format(self.__com1Freq['stby']) + "MHz")
                self.__lastRefreshTime = time.time()

    """
    swap freq using x-plane internal flip function of com1
    """
    def __SwitchFreq(self, gpioPin):
        self.__queue.hardwaretonetwork.put("sim/radios/com1_standy_flip")

    def __CoarseCLKChange(self, gpioPin):
        self.__coarseCLKCounter += 1
        if self.__coarseDTCounter > 0:
            self.__queue.hardwaretonetwork.put("sim/radios/stby_com1_coarse_up")
            self.__coarseCLKCounter = 0
            self.__coarseDTCounter = 0

    def __FineCLKChange(self, gpioPin):
        self.__fineCLKCounter += 1
        if self.__fineDTCounter > 0:
            self.__queue.hardwaretonetwork.put("sim/radios/stby_com1_fine_up_833")
            self.__fineCLKCounter = 0
            self.__fineDTCounter = 0

    def __CoarseDTChange(self, gpioPin):
        self.__coarseDTCounter += 1
        if self.__coarseCLKCounter > 0:
            self.__queue.hardwaretonetwork.put("sim/radios/stby_com1_coarse_down")
            self.__coarseCLKCounter = 0
            self.__coarseDTCounter = 0


    def __FineDTChange(self, gpioPin):
        self.__fineDTCounter += 1
        if self.__fineCLKCounter > 0:
            self.__queue.hardwaretonetwork.put("sim/radios/stby_com1_fine_down_833")
            self.__fineCLKCounter = 0
            self.__fineDTCounter = 0
