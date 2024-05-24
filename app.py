from HandDetector import HandDetector
from ServoSignaler import ServoSignaler
from Bluetooth import Bluetooth

from cv2 import VideoCapture, flip, cvtColor, COLOR_BGR2RGB, putText, FONT_HERSHEY_SIMPLEX, imshow, waitKey, destroyAllWindows

def processBluetoothData(data: str):
    print(data)

def otherMain():
    bluetoothClient = Bluetooth("Raspberry Pi", processBluetoothData)

    bluetoothClient.send("Servo Signaler connected")
    servoSignaler = ServoSignaler([13, 16, 19, 20, 21, 26])

    angles = [0, 45, 90, 135, 180]

    if len(angles) == 6:
        for angle in angles:
            servoSignaler.moveOneServo(angle, angles[angle])

    bluetoothClient.stop()

def main():
    videoCapture = VideoCapture(0)
    handDetector = HandDetector()
    servoSignaler = ServoSignaler([
        13,
        16,
        19,
        20,
        21,
        26
    ])

    while videoCapture.isOpened():
        hasFrame, frame = videoCapture.read()

        if not hasFrame:
            raise Exception("No frame captured")
        
        frameRGB = cvtColor(frame, COLOR_BGR2RGB)
        frame = flip(frame, 1)

        handDetector.detectHands(frameRGB)

        handsLandmarks = handDetector.getResult()

        if handsLandmarks is not None:
            totalHands = 0
            for handLandmarks in handsLandmarks:
                fingersUp = handDetector.countHandFingers(handLandmarks)
                hand = handDetector.getHand(handLandmarks)

                handDetector.drawHand(frame, handLandmarks)

                putText(frame, f"{hand}: {fingersUp} fingers up", (10, 30 + totalHands * 40), FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                totalHands += 1

        imshow('Hand Tracking', frame)

        if waitKey(1) & 0xFF == ord('q'):
            break
    
    handDetector.close()
    videoCapture.release()
    servoSignaler.stopAllServos()
    destroyAllWindows()

if __name__ == "__main__":
    main()