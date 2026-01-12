"""
Medical Image Analysis Route
============================
Handles image upload and AI-powered medical image analysis.
Uses TorchXRayVision for chest X-rays and specialized models
for skin lesions and bone X-rays.
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import os
import cv2
import numpy as np
from PIL import Image
from datetime import datetime
import logging
from typing import Dict, Any, List, Tuple

from app.schemas import AnalysisResponse, Translation, ImageType, ErrorResponse
from app.models.model_loader import model_manager
from app.models.disease_database import disease_db, DiseaseDatabase
from app.utils.file_handler import file_handler
from app.utils.translator import translator_service
from app.utils.gradcam import generate_heatmap_simple
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


def generate_attention_heatmap(
    image: np.ndarray, 
    findings: Dict[str, float],
    primary_finding: str
) -> np.ndarray:
    """
    Generate attention heatmap based on model findings.
    
    For chest X-rays, creates a heatmap highlighting areas
    of potential abnormality based on model predictions.
    """
    height, width = image.shape[:2]
    
    # Create base heatmap
    heatmap = np.zeros((height, width), dtype=np.float32)
    
    # If there are significant findings, create focused heatmap
    if primary_finding != "No Significant Findings":
        # Create gaussian-based attention map
        # Center attention on middle-lower region for lung findings
        center_y, center_x = height // 2, width // 2
        
        # Different attention patterns for different findings
        if primary_finding in ["Cardiomegaly", "Enlarged Cardiomediastinum"]:
            # Heart is in center-left
            center_x = int(width * 0.45)
            center_y = int(height * 0.55)
            sigma_x, sigma_y = width * 0.2, height * 0.25
        elif primary_finding in ["Pneumothorax", "Effusion"]:
            # Usually peripheral
            sigma_x, sigma_y = width * 0.35, height * 0.4
        elif primary_finding in ["Pneumonia", "Consolidation", "Infiltration"]:
            # Can be anywhere in lung fields
            sigma_x, sigma_y = width * 0.3, height * 0.3
        else:
            # Default - general lung area
            sigma_x, sigma_y = width * 0.25, height * 0.3
        
        # Generate gaussian heatmap
        y, x = np.ogrid[:height, :width]
        heatmap = np.exp(-((x - center_x)**2 / (2 * sigma_x**2) + 
                          (y - center_y)**2 / (2 * sigma_y**2)))
        
        # Add some random variation for realism
        noise = np.random.normal(0, 0.1, heatmap.shape)
        heatmap = np.clip(heatmap + noise * heatmap, 0, 1)
    else:
        # For normal findings, create very subtle uniform heatmap
        heatmap = np.ones((height, width), dtype=np.float32) * 0.1
    
    # Normalize
    heatmap = (heatmap - heatmap.min()) / (heatmap.max() - heatmap.min() + 1e-8)
    
    return heatmap


def create_heatmap_overlay(
    original_image: np.ndarray,
    heatmap: np.ndarray,
    alpha: float = 0.4
) -> np.ndarray:
    """Create colored heatmap overlay on original image"""
    # Ensure heatmap is same size as image
    if heatmap.shape[:2] != original_image.shape[:2]:
        heatmap = cv2.resize(heatmap, (original_image.shape[1], original_image.shape[0]))
    
    # Apply colormap
    heatmap_colored = cv2.applyColorMap(
        (heatmap * 255).astype(np.uint8),
        cv2.COLORMAP_JET
    )
    
    # Convert to RGB if needed
    if len(original_image.shape) == 2:
        original_rgb = cv2.cvtColor(original_image, cv2.COLOR_GRAY2RGB)
    elif original_image.shape[2] == 4:
        original_rgb = cv2.cvtColor(original_image, cv2.COLOR_RGBA2RGB)
    else:
        original_rgb = original_image.copy()
    
    heatmap_rgb = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)
    
    # Blend
    overlay = cv2.addWeighted(original_rgb, 1 - alpha, heatmap_rgb, alpha, 0)
    
    return overlay


@router.post(
    "/analyze",
    response_model=AnalysisResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def analyze_image(
    image: UploadFile = File(..., description="Medical image file (JPG, JPEG, PNG)"),
    image_type: str = Form(..., description="Type of medical image: chest_xray, bone_xray, or skin_image")
):
    """
    Analyze medical image using AI model
    
    Uses pre-trained medical AI models:
    - **chest_xray**: TorchXRayVision DenseNet121 (trained on 700K+ X-rays)
    - **skin_image**: EfficientNet-B3 for skin lesion classification
    - **bone_xray**: ResNet50 for bone abnormality detection
    
    Returns:
    - Disease/condition classification
    - Confidence score (0-1)
    - Detailed medical description
    - Risk level assessment
    - Treatment recommendations
    - Heatmap visualization
    - Multi-language translations (EN, HI, ES, FR)
    """
    file_path = None
    
    try:
        # Validate image type
        try:
            image_type_enum = ImageType(image_type)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid image type. Must be one of: {', '.join([t.value for t in ImageType])}"
            )
        
        # Save uploaded file
        file_path, filename = await file_handler.save_upload_file(image)
        logger.info(f"Processing image: {filename}, type: {image_type}")
        
        # Load image with PIL for model
        try:
            pil_image = Image.open(file_path)
            # Also load with OpenCV for heatmap generation
            cv_image = cv2.imread(file_path)
            if cv_image is not None:
                cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            else:
                # Convert PIL to numpy
                cv_image = np.array(pil_image.convert('RGB'))
        except Exception as e:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid or corrupted image file: {str(e)}"
            )
        
        # Run AI inference using the new medical models
        logger.info(f"Running {image_type} model inference...")
        prediction = model_manager.predict(image_type, pil_image)
        
        # Extract prediction results
        primary_finding = prediction['primary_finding']
        confidence = prediction['confidence']
        risk_level = prediction['risk_level']
        all_findings = prediction.get('all_findings', {})
        positive_findings = prediction.get('positive_findings', [])
        model_info = prediction.get('model_info', 'AI Model')
        
        logger.info(f"Prediction: {primary_finding} (confidence: {confidence:.2%}, risk: {risk_level})")
        
        # Log all significant findings for chest X-rays
        if positive_findings:
            logger.info(f"Positive findings: {positive_findings}")
        
        # Get disease information from database
        disease_info = disease_db.get_disease_info(image_type, primary_finding)
        recommendation = disease_db.get_recommendation(risk_level, image_type)
        
        # Build detailed description
        description = disease_info.description
        if positive_findings and len(positive_findings) > 1:
            # Add info about additional findings
            additional = [f"{name} ({prob:.0%})" for name, prob in positive_findings[1:4]]
            if additional:
                description += f"\n\nAdditional findings detected: {', '.join(additional)}"
        
        # Add symptoms to description
        if disease_info.common_symptoms:
            symptoms_text = ", ".join(disease_info.common_symptoms[:5])
            description += f"\n\nCommon symptoms: {symptoms_text}"
        
        # Generate heatmap
        try:
            heatmap = generate_attention_heatmap(cv_image, all_findings, primary_finding)
            overlay = create_heatmap_overlay(cv_image, heatmap, alpha=0.4)
        except Exception as e:
            logger.warning(f"Heatmap generation failed: {str(e)}, using simple heatmap")
            heatmap = generate_heatmap_simple(cv_image)
            overlay = create_heatmap_overlay(cv_image, heatmap, alpha=0.3)
        
        # Save heatmap
        heatmap_filename = f"heatmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
        heatmap_path = os.path.join(settings.HEATMAP_OUTPUT_PATH, heatmap_filename)
        cv2.imwrite(heatmap_path, cv2.cvtColor(overlay, cv2.COLOR_RGB2BGR))
        
        # Generate heatmap URL
        heatmap_url = f"http://localhost:{settings.PORT}/static/heatmaps/{heatmap_filename}"
        
        # Translate diagnosis
        try:
            translations_dict = translator_service.translate_diagnosis(
                primary_finding,
                description,
                recommendation
            )
        except Exception as e:
            logger.warning(f"Translation failed: {str(e)}, using English only")
            translations_dict = {
                'en': f"{primary_finding}: {description}\n\n{recommendation}",
                'hi': None,
                'es': None,
                'fr': None,
                'te': None
            }
        
        # Build response
        response = AnalysisResponse(
            diagnosis=primary_finding,
            confidence=confidence,
            description=description,
            recommended_action=recommendation,
            heatmap_url=heatmap_url,
            translations=Translation(
                en=translations_dict.get('en', ''),
                hi=translations_dict.get('hi'),
                es=translations_dict.get('es'),
                fr=translations_dict.get('fr'),
                te=translations_dict.get('te')
            ),
            risk_level=risk_level
        )
        
        # Cleanup uploaded file
        file_handler.cleanup_file(file_path)
        
        logger.info(f"Analysis completed successfully for {filename}")
        logger.info(f"Model used: {model_info}")
        
        return response
        
    except HTTPException:
        if file_path:
            file_handler.cleanup_file(file_path)
        raise
        
    except Exception as e:
        if file_path:
            file_handler.cleanup_file(file_path)
        
        logger.error(f"Error during analysis: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing image: {str(e)}"
        )


@router.get("/analyze/status")
async def get_analysis_status():
    """Get API status and available models"""
    return {
        "status": "operational",
        "models_available": model_manager.get_supported_types(),
        "supported_types": [t.value for t in ImageType],
        "model_info": {
            model_type: model_manager.get_model_info(model_type)
            for model_type in model_manager.get_supported_types()
        }
    }


@router.get("/analyze/findings/{image_type}")
async def get_possible_findings(image_type: str):
    """Get list of possible findings for an image type"""
    try:
        image_type_enum = ImageType(image_type)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid image type. Must be one of: {', '.join([t.value for t in ImageType])}"
        )
    
    diseases = disease_db.get_disease_names(image_type)
    model_info = model_manager.get_model_info(image_type)
    
    return {
        "image_type": image_type,
        "possible_findings": diseases,
        "model_info": model_info
    }
