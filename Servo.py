import RPi.GPIO as GPIO
import time

class Servo:
    __motor: GPIO.PWM
    __home: float = 7.5

    def __init__(self, motorPin: int, frequency: int = 50) -> None:
        self.__motor = GPIO.PWM(motorPin, frequency)
        self.__motor.start(self.__home)

    def move(self, angle: float)-> None:
        self.__motor.ChangeDutyCycle((45 + angle) / 18)
        time.sleep(0.5)
        return
    
    def stop(self):
        self.__motor.stop()
        return