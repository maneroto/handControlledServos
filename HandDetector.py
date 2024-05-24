from mediapipe.python.solutions.hands import Hands, NamedTuple, HAND_CONNECTIONS
from mediapipe.tasks.python.vision.hand_landmarker import HandLandmark
from mediapipe.python.solutions.drawing_utils import draw_landmarks
from mediapipe.tasks.python.components.containers import NormalizedLandmark
from cv2 import cvtColor, COLOR_BGR2RGB
from cv2.typing import MatLike
from typing import List

from config.settings import MODEL_HANDS_TO_DETECT

FINGER_TIPS = [HandLandmark.INDEX_FINGER_TIP, HandLandmark.MIDDLE_FINGER_TIP, HandLandmark.RING_FINGER_TIP, HandLandmark.PINKY_TIP, HandLandmark.THUMB_TIP]

class HandDetector:
    __detector: Hands
    __result: NamedTuple | None

    def __init__(self):
        self.__detector = Hands(static_image_mode=False, max_num_hands=MODEL_HANDS_TO_DETECT, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.__result = None

    def getResult(self):
        return self.__result

    def detectHands(self, frame: MatLike):
        # Convert the frame to RGB
        frameRGB = cvtColor(frame, COLOR_BGR2RGB)

        # Detect hands
        self.__result = self.__detector.process(frameRGB).multi_hand_landmarks # type: ignore

        return
        
    def countHandFingers(self, handLandmarks: List[NormalizedLandmark], tolerance: float = 0.1):
        fingersUp = 0

        for fingerTip in FINGER_TIPS:
            downEdge = fingerTip - 2
            # Treat the thumb differently because it has only 2 points, so the down edge is the index finger metacarpal
            if fingerTip == HandLandmark.THUMB_TIP:
                downEdge = HandLandmark.INDEX_FINGER_MCP
            
            # Check if the finger tip is above the down edge of the finger
            isDown = handLandmarks.landmark[fingerTip].y < handLandmarks.landmark[downEdge].y - (tolerance * handLandmarks.landmark[downEdge].z) # type: ignore
            
            if isDown:
                fingersUp += 1

        return fingersUp
    
    def drawHand(self, frame: MatLike, handLandmarks: List[NormalizedLandmark]):
        draw_landmarks(frame, handLandmarks, HAND_CONNECTIONS) # type: ignore
    
    def getHand(self, handLandmarks: List[NormalizedLandmark]):
        # Check if the hand is right or left by comparing the x position of the index and pinky finger tips
        return "right" if handLandmarks.landmark[HandLandmark.INDEX_FINGER_TIP].x < handLandmarks.landmark[HandLandmark.PINKY_TIP].x else "left" # type: ignore
    
    def close(self):
        self.__detector.close()