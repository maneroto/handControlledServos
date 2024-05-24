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

    def addServo(self, servoPin: int) -> None:
        if len(self.__servos) >= self.__maxServos:
            raise Exception(f"Cannot add more than {self.__maxServos} servos")
        
        self.__servos.append(Servo(servoPin))
        return

    def removeServo(self, servo: Servo | None = None) -> None:
        if servo is None:
            self.__servos.pop()
            return
        
        self.__servos.remove(servo)

        print(f'Servo at pin {servo.getPin()} removed') 
        return
    
    def stopOneServo(self, index: int) -> None:
        if index > len(self.__servos):
            raise Exception("Servo index out of range")

        self.__servos[index].stop()
        return
    
    def stopAllServos(self) -> None:
        for servo in self.__servos:
            servo.stop()
        return
    
    def getServos(self) -> list[Servo]:
        return self.__servos

    def moveServo(self, servo: Servo, angle: float) -> None:
        servo.move(angle)
        print(f'Moving servo at pin {servo.getPin()} to {angle} degrees')
        return
    
    # Function to signal a servo by its index in the list
    def moveOneServo(self, index: int, angle: float) -> None:
        if index > len(self.__servos):
            raise Exception("Servo index out of range")

        self.moveServo(self.__servos[index], angle)
        
        return
    
    def moveAllServos(self, angle: float) -> None:
        for servo in self.__servos:
            self.moveServo(servo, angle)
        return