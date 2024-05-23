from mediapipe import Image, ImageFormat
from mediapipe.tasks.python.vision import RunningMode
from mediapipe.tasks.python.vision.hand_landmarker import HandLandmark, HandLandmarker, HandLandmarkerOptions, HandLandmarkerResult, HandLandmarksConnections
from mediapipe.tasks.python import BaseOptions
from config.settings import MODEL_HAND_DETECTOR, MODEL_HANDS_TO_DETECT
from cv2 import flip, cvtColor, COLOR_BGR2RGB, line, circle
from mediapipe.tasks.python.components.containers import NormalizedLandmark
from cv2.typing import MatLike
from typing import List
from time import time

FINGER_TIPS = [HandLandmark.INDEX_FINGER_TIP, HandLandmark.MIDDLE_FINGER_TIP, HandLandmark.RING_FINGER_TIP, HandLandmark.PINKY_TIP, HandLandmark.THUMB_TIP]

class HandDetector:
    __detector: HandLandmarker
    __result: List[List[NormalizedLandmark]] | None

    def __init__(self):
        options = HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=MODEL_HAND_DETECTOR),
            running_mode=RunningMode.LIVE_STREAM,
            result_callback=self.updateResult, 
            num_hands=MODEL_HANDS_TO_DETECT
        )
        self.__detector = HandLandmarker.create_from_options(options)
        self.__result = None

    def updateResult(self, result: HandLandmarkerResult, output_image: Image, timestamp_ms: int):
        self.__result = result.hand_landmarks
        del output_image, timestamp_ms

    def getResult(self):
        return self.__result

    def detectHands(self, frame: MatLike):
        # Flip the frame horizontally for a later selfie-view display
        frame = flip(frame, 1)

        # Convert the frame to RGB
        frameRGB = cvtColor(frame, COLOR_BGR2RGB)

        image = Image(image_format=ImageFormat.SRGB, data=frameRGB)

        # Detect hands asynchronously
        self.__detector.detect_async(image, timestamp_ms = int(time() * 1000))

        return
        
    def countHandFingers(self, handLandmarks: List[NormalizedLandmark], tolerance: float = 0.1):
        fingersUp = 0

        for fingerTip in FINGER_TIPS:
            downEdge = fingerTip - 2
            # Treat the thumb differently because it has only 2 points, so the down edge is the index finger metacarpal
            if fingerTip == HandLandmark.THUMB_TIP:
                downEdge = HandLandmark.INDEX_FINGER_MCP
            
            # Check if the finger tip is above the down edge of the finger
            isDown = handLandmarks[fingerTip].y < handLandmarks[downEdge].y - (tolerance * handLandmarks[downEdge].z)
            
            if isDown:
                fingersUp += 1

        return fingersUp
    
    def drawHand(self, frame: MatLike, handLandmarks: List[NormalizedLandmark]):
        # Draw the landmarks and connections
        for connection in HandLandmarksConnections.HAND_CONNECTIONS:
            # Get the start and end points of the connection
            start = connection.start
            end = connection.end

            # Get the x and y coordinates of the start and end points
            x0, y0 = int(handLandmarks[start].x * frame.shape[1]), int(handLandmarks[start].y * frame.shape[0])
            x1, y1 = int(handLandmarks[end].x * frame.shape[1]), int(handLandmarks[end].y * frame.shape[0])

            # Draw the connection line and the start point of the connection
            circle(frame, (x0, y0), 5, (0, 0, 255), -1)
            line(frame, (x0, y0), (x1, y1), (255, 0, 0), 2)

        # As the tips are landmarks, we can draw them as circles
        for fingerTip in FINGER_TIPS:
            x, y = int(handLandmarks[fingerTip].x * frame.shape[1]), int(handLandmarks[fingerTip].y * frame.shape[0])
            circle(frame, (x, y), 5, (0, 0, 255), -1)
    
    def getHand(self, handLandmarks: List[NormalizedLandmark]):
        # Check if the hand is right or left by comparing the x position of the index and pinky finger tips
        return "right" if handLandmarks[HandLandmark.INDEX_FINGER_TIP].x < handLandmarks[HandLandmark.PINKY_TIP].x else "left"
    
    def close(self):
        self.__detector.close()