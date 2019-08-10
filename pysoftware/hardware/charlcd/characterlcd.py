"""
Use RPLCD to power the LCD, later use the own driver
"""

from RPLCD.i2c import CharLCD  # pylint: disable=import-error

class CharacterLCD():
    def __init__(self, chip, i2cbus, i2caddress, col, row):
        self.__lcd = CharLCD(i2c_expander=chip, address=i2caddress, port=i2cbus, cols=col, rows=row)

    def WriteString(self, text):
        self.__lcd.clear()
        self.__lcd.write_string(text)
        
    def WriteLines(self, textArray, numberOfLines):
        self.__lcd.clear()
        self.__lcd.write_string(textArray[0])
        for i in range(1, numberOfLines):
            # self.__lcd.crlf()
            self.__lcd.write_string("\n\r")
            self.__lcd.write_string(textArray[i])

    def Clean(self):
        self.__lcd.clear()