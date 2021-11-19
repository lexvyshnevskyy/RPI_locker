import RPi.GPIO as GPIO
import time
channel = [26, 20, 21]
Relay_Ch1 = channel[0]
Relay_Ch2 = channel[1]
Relay_Ch3 = channel[2]

class Relay:
    """
    class for working with lock
    """
    status = None

    def __init__(self):
        try:
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)

            GPIO.setup(Relay_Ch1, GPIO.OUT)
            GPIO.setup(Relay_Ch2, GPIO.OUT)
            GPIO.setup(Relay_Ch3, GPIO.OUT)
            for ch in channel:
                print("Channel ", ch, ":The Common Contact is access to the Normal Open Contact!")
                GPIO.output(ch, GPIO.LOW)
                time.sleep(0.5)
                print("Channel ", ch, ":The Common Contact is access to the Normal Closed Contact!\n")
                GPIO.output(ch, GPIO.HIGH)
            #threading.Thread(target=self.lock_pooling).start()
        except Exception as e:
            print('relay init', e)
            self.__exit__()
            return
        print("Setup The Relay Module is [success]")
        self.status = False

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.status = None
        GPIO.cleanup()

    def lock(self,ch_number):
        print(channel[ch_number])
        GPIO.output(channel[ch_number], GPIO.LOW)
        self.status = True
        time.sleep(5)
        GPIO.output(channel[ch_number], GPIO.HIGH)
        self.status = False