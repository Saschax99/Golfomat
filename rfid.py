# https://tutorials-raspberrypi.de/raspberry-pi-rfid-rc522-tueroeffner-nfc/

import sys
if not "win" in sys.platform: 
    import RPi.GPIO as GPIO
    from mfrc522 import SimpleMFRC522
    
class rfid:
   
    def write():
        try:
            reader = SimpleMFRC522()
            text = input('Enter tag data:')
            print("Hold tag to module")
            reader.write(text)
            print("Done...")
        finally:
            if not "win" in sys.platform: GPIO.cleanup()
                
    def read():
        if not "win" in sys.platform:
            try:
                reader = SimpleMFRC522()
                # id, text = reader.read()
                text = reader.read()
                print(id)
                print(text)
                # return id, text
                return text[1]
            finally:
                GPIO.cleanup()
        else:
            print("reading")
