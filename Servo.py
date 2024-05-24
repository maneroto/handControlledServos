import RPi.GPIO as GPIO
import time

class Servo:
    __motor: GPIO.PWM
    __pin: int
    __minAngle: float
    __maxAngle: float
    __angle: float
    __home: float
    __sleepTime: float

    def __init__(self, motorPin: int, initialAngle: float = 90, minAngle: float = 0, maxAngle = 180, sleepTime: float = 2, frequency: int = 50) -> None:
        self.__sleepTime = sleepTime
        self.__minAngle = minAngle
        self.__maxAngle = maxAngle
        self.__angle = self.__clampAngle(initialAngle)
        self.__home = (45 + self.__angle) / 18
        self.__pin = motorPin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(motorPin, GPIO.OUT)
        self.__motor = GPIO.PWM(motorPin, frequency)
        self.__motor.start(self.__home)

    def __clampAngle(self, angle: float) -> float:
        return max(self.__minAngle, min(angle, self.__maxAngle))
    
    def goHome(self):
        self.__motor.ChangeDutyCycle(self.__home)
        time.sleep(self.__sleepTime)
        return
    
    def getAngle(self) -> float:
        return self.__angle
    

    def move(self, angle: float)-> None:
        angle = self.__clampAngle(angle)
        self.__angle = angle
        self.__motor.ChangeDutyCycle((45 + angle) / 18)
        time.sleep(self.__sleepTime)
        return
    
    def getPin(self) -> int:
        return self.__pin

    def stop(self):
        self.__motor.stop()
        GPIO.cleanup()
        return