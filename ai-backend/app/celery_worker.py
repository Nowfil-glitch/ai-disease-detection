from celery import Celery
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Initialize Celery
celery_app = Celery(
    'ai_disease_detection',
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

# Celery configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,  # 5 minutes max per task
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=100
)


@celery_app.task(name='analyze_image_async')
def analyze_image_async(image_path: str, image_type: str):
    """
    Asynchronous image analysis task
    
    Args:
        image_path: Path to the uploaded image
        image_type: Type of medical image
        
    Returns:
        Analysis results dictionary
    """
    try:
        from app.models.model_loader import model_manager
        from app.models.disease_database import disease_db
        from app.utils.image_processor import image_processor
        
        logger.info(f"Starting async analysis for {image_path}")
        
        # Preprocess image
        image_tensor, original_image = image_processor.preprocess_image(image_path)
        
        # Run inference
        prediction = model_manager.predict(image_type, image_tensor)
        
        # Get disease info
        class_names = model_manager.get_class_names(image_type)
        disease_name = class_names.get(prediction['predicted_class'], "Unknown")
        
        logger.info(f"Async analysis completed: {disease_name}")
        
        return {
            "diagnosis": disease_name,
            "confidence": prediction['confidence'],
            "status": "completed"
        }
        
    except Exception as e:
        logger.error(f"Error in async analysis: {str(e)}")
        return {
            "status": "failed",
            "error": str(e)
        }


if __name__ == '__main__':
    celery_app.start()
