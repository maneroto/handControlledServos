from HandDetector import HandDetector

from cv2 import VideoCapture, flip, cvtColor, COLOR_BGR2RGB, putText, FONT_HERSHEY_SIMPLEX, imshow, waitKey, destroyAllWindows

def main():
    videoCapture = VideoCapture(0)
    handDetector = HandDetector()

    while videoCapture.isOpened():
        hasFrame, frame = videoCapture.read()

        if not hasFrame:
            raise Exception("No frame captured")
        
        frame = flip(frame, 1)

        handDetector.detectHands(frame)

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
    destroyAllWindows()

if __name__ == "__main__":
    main()