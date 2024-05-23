from gpiozero import Servo

class ServoSignaler:
    __servos: list[Servo]

    def __init__(self, servos: list[Servo] = []):
        self.__servos = servos

    def addServo(self, servoPin: int):
        if len(self.__servos) >= 5:
            raise Exception("Cannot add more than 5 servos")
        
        self.__servos.append(Servo(servoPin))
        return

    def removeServo(self, servo: Servo | None = None):
        if servo is None:
            self.__servos.pop()
            return
        
        self.__servos.remove(servo)
        return
    
    def getServos(self):
        return self.__servos
    

    def signalServo(self, servo: Servo, angle: float):
        servo.value = angle / 180
        return
    
    # Function to signal a servo by its index in the list
    def signalServoByIndex(self, index: int, angle: float):
        if index > len(self.__servos):
            raise Exception("Servo index out of range")

        self.signalServo(self.__servos[index], angle)
        
        return