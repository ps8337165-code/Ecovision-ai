import cv2
from ultralytics import YOLO
from app.config import settings

class EcoVisionDetector:
    def _init_(self):
        # Load YOLO model
        self.model = YOLO(settings.MODEL_PATH)

    def process_frame(self, frame):
        """
        Processes a video frame with YOLO, overlays detection boxes,
        and prints the dynamic priority score.
        """
        # Run YOLO detection
        results = self.model(frame, conf=settings.CONFIDENCE_THRESHOLD)[0]

        # Draw object detection boxes
        annotated_frame = results.plot()

        # Dynamic priority score calculation based on detected items
        num_detections = len(results.boxes)
        priority_score = min(100.0, num_detections * 20.0)

        # Draw green Priority Score overlay on screen
        cv2.putText(
            annotated_frame, 
            f"Priority Score: {priority_score:.1f}%", 
            (30, 50), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            1.0, 
            (0, 255, 0), 
            2
        )

        return annotated_frame, priority_score

detector = EcoVisionDetector()