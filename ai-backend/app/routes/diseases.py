from fastapi import APIRouter
from app.schemas import SupportedDiseasesResponse, ImageType
from app.models.disease_database import disease_db

router = APIRouter()


@router.get(
    "/diseases",
    response_model=SupportedDiseasesResponse,
    summary="Get supported diseases",
    description="Retrieve list of all diseases that can be detected by the AI models"
)
async def get_supported_diseases():
    """
    Get all supported diseases organized by image type
    
    Returns:
    - List of diseases for each medical image type
    - Disease descriptions
    - Common symptoms
    """
    diseases = disease_db.get_all_diseases_by_type()
    return SupportedDiseasesResponse(types=diseases)


@router.get(
    "/diseases/{image_type}",
    summary="Get diseases by type",
    description="Get diseases for a specific medical image type"
)
async def get_diseases_by_type(image_type: ImageType):
    """
    Get diseases for a specific image type
    
    - **image_type**: Type of medical image (chest_xray, bone_xray, skin_image)
    """
    diseases = disease_db.get_all_diseases_by_type()
    return {
        "image_type": image_type.value,
        "diseases": diseases.get(image_type.value, [])
    }
