from Servo import Servo

class ServoSignaler:
    __servos: list[Servo]
    __maxServos: int

    def __init__(self, servosPins: list[int] = [], maxServos: int = 5) -> None:
        servos = []
        for servoPin in servosPins:
            servos.append(Servo(servoPin))
        self.__maxServos = maxServos if maxServos >= len(servosPins) else len(servosPins)
        self.__servos = servos

    def addServo(self, servoPin: int):
        if len(self.__servos) >= self.__maxServos:
            raise Exception(f"Cannot add more than {self.__maxServos} servos")
        
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
        servo.move(angle)
        return
    
    # Function to signal a servo by its index in the list
    def signalServoByIndex(self, index: int, angle: float):
        if index > len(self.__servos):
            raise Exception("Servo index out of range")

        self.signalServo(self.__servos[index], angle)
        
        return