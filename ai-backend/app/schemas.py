from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, List
from enum import Enum


class ImageType(str, Enum):
    """Supported medical image types"""
    CHEST_XRAY = "chest_xray"
    BONE_XRAY = "bone_xray"
    SKIN_IMAGE = "skin_image"


class AnalysisRequest(BaseModel):
    """Request model for image analysis"""
    image_type: ImageType = Field(..., description="Type of medical image")
    
    class Config:
        json_schema_extra = {
            "example": {
                "image_type": "chest_xray"
            }
        }


class Translation(BaseModel):
    """Multi-language translation model"""
    en: str = Field(..., description="English translation")
    hi: Optional[str] = Field(None, description="Hindi translation")
    es: Optional[str] = Field(None, description="Spanish translation")
    fr: Optional[str] = Field(None, description="French translation")
    te: Optional[str] = Field(None, description="Telugu translation")


class AnalysisResponse(BaseModel):
    """Response model for image analysis"""
    diagnosis: str = Field(..., description="Detected disease or condition")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)")
    description: str = Field(..., description="Detailed description of the condition")
    recommended_action: str = Field(..., description="Recommended medical action")
    heatmap_url: str = Field(..., description="URL to the heatmap visualization")
    translations: Translation = Field(..., description="Multi-language translations")
    risk_level: str = Field(..., description="Risk level: low, moderate, high")
    disclaimer: str = Field(
        default="Educational/Informational use only. Not a substitute for professional medical advice.",
        description="Legal disclaimer"
    )
    
    @validator('confidence')
    def validate_confidence(cls, v):
        if not 0 <= v <= 1:
            raise ValueError('Confidence must be between 0 and 1')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "diagnosis": "Pneumonia",
                "confidence": 0.92,
                "description": "Pneumonia is an infection that inflames air sacs in one or both lungs.",
                "recommended_action": "Consult a pulmonologist. Take prescribed antibiotics.",
                "heatmap_url": "http://localhost:8000/static/heatmaps/abc123.png",
                "translations": {
                    "en": "Pneumonia detected, consult a doctor immediately.",
                    "hi": "निमोनिया का पता चला, तुरंत डॉक्टर से परामर्श करें।",
                    "es": "Se detectó neumonía, consulte a un médico de inmediato."
                },
                "risk_level": "high",
                "disclaimer": "Educational/Informational use only. Not a substitute for professional medical advice."
            }
        }


class DiseaseInfo(BaseModel):
    """Disease information model"""
    name: str
    description: str
    common_symptoms: List[str]
    
    
class SupportedDiseasesResponse(BaseModel):
    """Response model for supported diseases"""
    types: Dict[str, List[DiseaseInfo]]
    
    class Config:
        json_schema_extra = {
            "example": {
                "types": {
                    "chest_xray": [
                        {
                            "name": "Pneumonia",
                            "description": "Lung infection causing inflammation",
                            "common_symptoms": ["Cough", "Fever", "Difficulty breathing"]
                        }
                    ],
                    "bone_xray": [
                        {
                            "name": "Fracture",
                            "description": "Break in bone continuity",
                            "common_symptoms": ["Pain", "Swelling", "Deformity"]
                        }
                    ],
                    "skin_image": [
                        {
                            "name": "Melanoma",
                            "description": "Serious type of skin cancer",
                            "common_symptoms": ["Irregular mole", "Color changes", "Bleeding"]
                        }
                    ]
                }
            }
        }


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "Invalid file type",
                "detail": "Only JPG, JPEG, and PNG files are allowed"
            }
        }
