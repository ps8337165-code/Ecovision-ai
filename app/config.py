import os
from pydantic import BaseModel

class Settings(BaseModel):
    PROJECT_NAME: str = "EcoVision AI Prototype"
    VERSION: str = "1.0.0"
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    
    MODEL_PATH: str = os.getenv("MODEL_PATH", "yolov8n.pt")
    CONFIDENCE_THRESHOLD: float = 0.4
    
    WEIGHT_FILL: float = 0.6
    WEIGHT_LITTER: float = 0.4

settings = Settings()