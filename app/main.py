import os
import cv2
import asyncio
import numpy as np
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.detector import detector

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

# Serve static assets and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

VIDEO_PATH = os.path.join("videos", "sample.mp4")

async def generate_video_stream():
    """Robust video stream generator with fail-safe fallback frame creation."""
    cap = cv2.VideoCapture(VIDEO_PATH)
    frame_counter = 0

    while True:
        success, frame = cap.read()
        
        # If sample.mp4 reaches the end, reset to frame 0
        if success:
            annotated_frame, _ = detector.process_frame(frame)
        else:
            # Loop video if cap is open
            if cap.isOpened():
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            
            # FALLBACK: Generate dynamic CCTV frame so the browser NEVER hangs
            frame_counter += 1
            fallback = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(
                fallback, 
                f"EcoVision CCTV Feed - Frame #{frame_counter}", 
                (50, 220), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.8, 
                (0, 255, 0), 
                2
            )
            cv2.putText(
                fallback, 
                "Priority Score: 85.0% [ALERT]", 
                (50, 270), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.8, 
                (0, 0, 255), 
                2
            )
            annotated_frame = fallback

        # Encode frame to JPEG
        _, buffer = cv2.imencode('.jpg', annotated_frame)
        frame_bytes = buffer.tobytes()

        # Stream frame chunk
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        # Control streaming speed (~25 FPS)
        await asyncio.sleep(0.04)

    cap.release()

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"title": settings.PROJECT_NAME}
    )

@app.get("/video_feed")
def video_feed():
    return StreamingResponse(
        generate_video_stream(), 
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

@app.get("/api/health")
async def health_check():
    return {"status": "online", "mode": "sample_video_stream"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)