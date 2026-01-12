"""
Medical Disease Database
========================
Comprehensive database of medical conditions detected by AI models.
Includes detailed descriptions, symptoms, and recommendations.

Supports:
- TorchXRayVision pathologies (18 chest conditions)
- ISIC skin lesion classes (8 skin conditions)
- Bone X-ray conditions (5 bone conditions)
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class DiseaseInfo:
    """Information about a medical condition"""
    name: str
    description: str
    common_symptoms: List[str]
    risk_category: str = "moderate"  # low, moderate, high
    specialist: str = "General Physician"
    icd10_code: Optional[str] = None


# ============================================
# Chest X-Ray Pathologies (TorchXRayVision)
# ============================================
CHEST_XRAY_DISEASES: Dict[str, DiseaseInfo] = {
    "No Significant Findings": DiseaseInfo(
        name="No Significant Findings",
        description="The chest X-ray analysis did not reveal any significant abnormalities. The lung fields appear clear, heart size is within normal limits, and no acute cardiopulmonary disease is identified.",
        common_symptoms=["None - routine screening or follow-up"],
        risk_category="low",
        specialist="General Physician",
        icd10_code="Z00.00"
    ),
    "Atelectasis": DiseaseInfo(
        name="Atelectasis",
        description="Atelectasis is a complete or partial collapse of the lung or a section of the lung. It occurs when the tiny air sacs (alveoli) within the lung become deflated or filled with fluid. This can reduce oxygen delivery to organs.",
        common_symptoms=["Difficulty breathing", "Rapid shallow breathing", "Coughing", "Chest pain", "Low oxygen saturation"],
        risk_category="moderate",
        specialist="Pulmonologist",
        icd10_code="J98.11"
    ),
    "Consolidation": DiseaseInfo(
        name="Consolidation",
        description="Pulmonary consolidation indicates that the air in the small airways has been replaced with fluid, pus, blood, cells, or other material. This is commonly seen in pneumonia and other lung infections.",
        common_symptoms=["Productive cough", "Fever", "Chest pain", "Difficulty breathing", "Fatigue"],
        risk_category="high",
        specialist="Pulmonologist",
        icd10_code="J18.9"
    ),
    "Infiltration": DiseaseInfo(
        name="Infiltration",
        description="Pulmonary infiltration refers to abnormal substances (fluid, cells, or inflammatory material) filling the air spaces or interstitial areas of the lungs. Can indicate infection, inflammation, or malignancy.",
        common_symptoms=["Cough", "Shortness of breath", "Fever", "Chest discomfort", "Fatigue"],
        risk_category="moderate",
        specialist="Pulmonologist",
        icd10_code="R91.8"
    ),
    "Pneumothorax": DiseaseInfo(
        name="Pneumothorax",
        description="Pneumothorax (collapsed lung) occurs when air leaks into the space between the lung and chest wall. This air pushes on the outside of the lung and makes it collapse. THIS IS A MEDICAL EMERGENCY if large or tension pneumothorax.",
        common_symptoms=["Sudden sharp chest pain", "Shortness of breath", "Rapid heart rate", "Cyanosis (bluish skin)", "Fatigue"],
        risk_category="high",
        specialist="Emergency Medicine / Thoracic Surgeon",
        icd10_code="J93.9"
    ),
    "Edema": DiseaseInfo(
        name="Pulmonary Edema",
        description="Pulmonary edema is excess fluid in the lungs, often due to heart failure. Fluid accumulates in the air sacs, making breathing difficult. Can be life-threatening if severe.",
        common_symptoms=["Extreme shortness of breath", "Feeling of suffocating", "Wheezing", "Anxiety", "Coughing pink frothy sputum", "Rapid heartbeat"],
        risk_category="high",
        specialist="Cardiologist / Pulmonologist",
        icd10_code="J81.0"
    ),
    "Emphysema": DiseaseInfo(
        name="Emphysema",
        description="Emphysema is a chronic lung condition where the air sacs (alveoli) are damaged, leading to shortness of breath. Part of COPD (Chronic Obstructive Pulmonary Disease), often caused by smoking.",
        common_symptoms=["Shortness of breath", "Chronic cough", "Wheezing", "Reduced exercise tolerance", "Barrel-shaped chest"],
        risk_category="moderate",
        specialist="Pulmonologist",
        icd10_code="J43.9"
    ),
    "Fibrosis": DiseaseInfo(
        name="Pulmonary Fibrosis",
        description="Pulmonary fibrosis is scarring and thickening of lung tissue. The scarring makes it hard to breathe and prevents adequate oxygen from reaching the bloodstream. Often progressive.",
        common_symptoms=["Shortness of breath", "Dry cough", "Fatigue", "Unexplained weight loss", "Aching muscles and joints", "Clubbing of fingers"],
        risk_category="high",
        specialist="Pulmonologist",
        icd10_code="J84.10"
    ),
    "Effusion": DiseaseInfo(
        name="Pleural Effusion",
        description="Pleural effusion is buildup of excess fluid between the layers of the pleura (membrane lining the lungs and chest cavity). Can be caused by infection, heart failure, cancer, or other conditions.",
        common_symptoms=["Shortness of breath", "Chest pain (pleuritic)", "Dry cough", "Difficulty breathing when lying down", "Fever if infectious"],
        risk_category="high",
        specialist="Pulmonologist",
        icd10_code="J90"
    ),
    "Pneumonia": DiseaseInfo(
        name="Pneumonia",
        description="Pneumonia is an infection that inflames the air sacs in one or both lungs. The air sacs may fill with fluid or pus, causing cough with phlegm, fever, chills, and difficulty breathing. Can be bacterial, viral, or fungal.",
        common_symptoms=["Cough with phlegm or pus", "Fever and chills", "Difficulty breathing", "Sharp chest pain when breathing", "Fatigue", "Nausea/vomiting"],
        risk_category="high",
        specialist="Pulmonologist / Infectious Disease Specialist",
        icd10_code="J18.9"
    ),
    "Pleural_Thickening": DiseaseInfo(
        name="Pleural Thickening",
        description="Pleural thickening is scarring and thickening of the pleura (lung lining). Often caused by asbestos exposure, infections, or inflammatory conditions. Can restrict lung expansion.",
        common_symptoms=["Shortness of breath", "Chest pain", "Chronic cough", "Reduced exercise capacity"],
        risk_category="moderate",
        specialist="Pulmonologist",
        icd10_code="J92.9"
    ),
    "Cardiomegaly": DiseaseInfo(
        name="Cardiomegaly",
        description="Cardiomegaly (enlarged heart) is not a disease itself but a sign of another condition. The heart can become enlarged due to high blood pressure, heart valve disease, cardiomyopathy, or other conditions.",
        common_symptoms=["Shortness of breath", "Swelling in legs/ankles", "Fatigue", "Irregular heartbeat", "Dizziness"],
        risk_category="moderate",
        specialist="Cardiologist",
        icd10_code="I51.7"
    ),
    "Nodule": DiseaseInfo(
        name="Pulmonary Nodule",
        description="A pulmonary nodule is a small, round growth on the lung. Most are benign (non-cancerous), but some may be early-stage lung cancer. Size, shape, and growth rate help determine malignancy risk. REQUIRES FOLLOW-UP.",
        common_symptoms=["Usually asymptomatic", "Occasionally cough", "Chest discomfort if large"],
        risk_category="high",
        specialist="Pulmonologist / Oncologist",
        icd10_code="R91.1"
    ),
    "Mass": DiseaseInfo(
        name="Lung Mass",
        description="A lung mass is a growth larger than 3cm in the lung. Lung masses have a higher probability of being cancerous than smaller nodules. URGENT evaluation required to determine if malignant.",
        common_symptoms=["Persistent cough", "Coughing up blood", "Chest pain", "Shortness of breath", "Unexplained weight loss", "Fatigue"],
        risk_category="high",
        specialist="Oncologist / Thoracic Surgeon",
        icd10_code="R91.8"
    ),
    "Hernia": DiseaseInfo(
        name="Hiatal Hernia",
        description="A hiatal hernia occurs when the upper part of the stomach pushes through an opening in the diaphragm into the chest cavity. May be visible on chest X-ray as abnormal shadow behind the heart.",
        common_symptoms=["Heartburn", "Regurgitation", "Difficulty swallowing", "Chest pain", "Feeling full quickly"],
        risk_category="low",
        specialist="Gastroenterologist",
        icd10_code="K44.9"
    ),
    "Lung Lesion": DiseaseInfo(
        name="Lung Lesion",
        description="A lung lesion is an abnormal area in the lung that may indicate infection, inflammation, or malignancy. Further imaging (CT scan) and possibly biopsy needed to characterize the lesion.",
        common_symptoms=["May be asymptomatic", "Cough", "Chest pain", "Shortness of breath", "Hemoptysis if advanced"],
        risk_category="high",
        specialist="Pulmonologist / Oncologist",
        icd10_code="R91.8"
    ),
    "Fracture": DiseaseInfo(
        name="Rib Fracture",
        description="Rib fractures are breaks in the rib bones, often caused by trauma. Can be seen on chest X-ray. Multiple fractures may affect breathing mechanics. Watch for complications like pneumothorax.",
        common_symptoms=["Sharp chest pain", "Pain worsens with breathing/coughing", "Tenderness over fracture site", "Bruising", "Difficulty taking deep breaths"],
        risk_category="moderate",
        specialist="Orthopedic Surgeon / Emergency Medicine",
        icd10_code="S22.3"
    ),
    "Lung Opacity": DiseaseInfo(
        name="Lung Opacity",
        description="Lung opacity refers to any area of increased density in the lung on X-ray. Can represent various conditions including infection, fluid, tumor, or atelectasis. Further evaluation needed.",
        common_symptoms=["Variable depending on cause", "Cough", "Shortness of breath", "Fever if infectious"],
        risk_category="moderate",
        specialist="Pulmonologist",
        icd10_code="R91.8"
    ),
    "Enlarged Cardiomediastinum": DiseaseInfo(
        name="Enlarged Cardiomediastinum",
        description="An enlarged cardiomediastinum indicates widening of the central chest structures (heart, great vessels, lymph nodes). Can be due to heart disease, aortic aneurysm, lymphoma, or other conditions.",
        common_symptoms=["Chest pain", "Shortness of breath", "Difficulty swallowing", "Hoarseness", "Swelling of face/arms"],
        risk_category="moderate",
        specialist="Cardiologist / Thoracic Surgeon",
        icd10_code="R93.1"
    ),
}

# ============================================
# Skin Lesion Classes (ISIC Dataset)
# ============================================
SKIN_LESION_DISEASES: Dict[str, DiseaseInfo] = {
    "Melanoma": DiseaseInfo(
        name="Melanoma",
        description="Melanoma is the most serious type of skin cancer, developing in the cells (melanocytes) that produce melanin. It can spread to other organs if not detected early. URGENT dermatological evaluation required.",
        common_symptoms=["New mole or changing mole", "Asymmetrical shape", "Irregular borders", "Multiple colors", "Diameter > 6mm", "Evolving size/shape/color"],
        risk_category="high",
        specialist="Dermatologist / Oncologist",
        icd10_code="C43.9"
    ),
    "Melanocytic Nevus": DiseaseInfo(
        name="Melanocytic Nevus (Mole)",
        description="A melanocytic nevus is a benign (non-cancerous) growth of melanocytes, commonly called a mole. Most moles are harmless, but should be monitored for changes using the ABCDE criteria.",
        common_symptoms=["Brown or black spot", "Round or oval shape", "Uniform color", "Stable size", "Usually smaller than 6mm"],
        risk_category="low",
        specialist="Dermatologist",
        icd10_code="D22.9"
    ),
    "Basal Cell Carcinoma": DiseaseInfo(
        name="Basal Cell Carcinoma",
        description="Basal cell carcinoma (BCC) is the most common form of skin cancer. It rarely spreads to other parts of the body but can cause significant local tissue destruction if untreated. Usually caused by sun exposure.",
        common_symptoms=["Pearly or waxy bump", "Flat flesh-colored lesion", "Bleeding or scabbing sore that heals and returns", "Scar-like area"],
        risk_category="high",
        specialist="Dermatologist / Dermatologic Surgeon",
        icd10_code="C44.91"
    ),
    "Actinic Keratosis": DiseaseInfo(
        name="Actinic Keratosis",
        description="Actinic keratosis (AK) is a rough, scaly patch on the skin caused by years of sun exposure. It's considered pre-cancerous - about 10% can progress to squamous cell carcinoma if left untreated.",
        common_symptoms=["Rough, scaly patch", "Flat to slightly raised", "Pink, red, or brown color", "Itching or burning", "Located on sun-exposed areas"],
        risk_category="moderate",
        specialist="Dermatologist",
        icd10_code="L57.0"
    ),
    "Benign Keratosis": DiseaseInfo(
        name="Benign Keratosis",
        description="Benign keratosis (including seborrheic keratosis) is a common non-cancerous skin growth. They are harmless growths that appear with age and do not require treatment unless bothersome.",
        common_symptoms=["Waxy, stuck-on appearance", "Brown, black, or tan color", "Slightly raised", "Round or oval shape", "Rough texture"],
        risk_category="low",
        specialist="Dermatologist",
        icd10_code="L82.1"
    ),
    "Dermatofibroma": DiseaseInfo(
        name="Dermatofibroma",
        description="Dermatofibroma is a common benign skin growth, often appearing on the legs. They are harmless fibrous nodules that may develop after minor injuries like insect bites.",
        common_symptoms=["Small firm bump", "Brown, red, or purple color", "Dimples when pinched", "Usually on legs", "May be slightly tender"],
        risk_category="low",
        specialist="Dermatologist",
        icd10_code="D23.9"
    ),
    "Vascular Lesion": DiseaseInfo(
        name="Vascular Lesion",
        description="Vascular lesions are abnormalities of blood vessels in the skin, including hemangiomas, cherry angiomas, and port-wine stains. Most are benign but should be evaluated if changing.",
        common_symptoms=["Red, purple, or blue discoloration", "May be flat or raised", "Blanches with pressure", "Variable size"],
        risk_category="low",
        specialist="Dermatologist",
        icd10_code="D18.01"
    ),
    "Squamous Cell Carcinoma": DiseaseInfo(
        name="Squamous Cell Carcinoma",
        description="Squamous cell carcinoma (SCC) is the second most common form of skin cancer. It can spread to other tissues if not treated. Usually caused by cumulative sun exposure.",
        common_symptoms=["Firm red nodule", "Flat lesion with scaly crust", "New sore on old scar", "Rough scaly patch on lip", "Red sore inside mouth"],
        risk_category="high",
        specialist="Dermatologist / Oncologist",
        icd10_code="C44.92"
    ),
}

# ============================================
# Bone X-Ray Conditions
# ============================================
BONE_XRAY_DISEASES: Dict[str, DiseaseInfo] = {
    "Normal": DiseaseInfo(
        name="Normal",
        description="No significant bone abnormalities detected. Bone density, alignment, and joint spaces appear within normal limits.",
        common_symptoms=["None - routine screening or follow-up"],
        risk_category="low",
        specialist="General Physician",
        icd10_code="Z00.00"
    ),
    "Fracture": DiseaseInfo(
        name="Fracture",
        description="A fracture is a break in bone continuity. Can range from hairline cracks to complete breaks. Treatment depends on location, type, and severity. May require immobilization or surgery.",
        common_symptoms=["Severe pain", "Swelling", "Bruising", "Deformity", "Inability to move affected area", "Tenderness"],
        risk_category="high",
        specialist="Orthopedic Surgeon",
        icd10_code="T14.8"
    ),
    "Osteoporosis": DiseaseInfo(
        name="Osteoporosis",
        description="Osteoporosis is a bone disease characterized by decreased bone density and mass, making bones fragile and more prone to fractures. Often called the 'silent disease' until a fracture occurs.",
        common_symptoms=["Often asymptomatic until fracture", "Back pain", "Loss of height over time", "Stooped posture", "Bones that break easily"],
        risk_category="moderate",
        specialist="Endocrinologist / Rheumatologist",
        icd10_code="M81.0"
    ),
    "Arthritis": DiseaseInfo(
        name="Arthritis",
        description="Arthritis refers to joint inflammation causing pain and stiffness. X-ray findings include joint space narrowing, bone spurs (osteophytes), and subchondral sclerosis.",
        common_symptoms=["Joint pain", "Stiffness", "Swelling", "Reduced range of motion", "Warmth around joint", "Morning stiffness"],
        risk_category="moderate",
        specialist="Rheumatologist / Orthopedic Surgeon",
        icd10_code="M19.90"
    ),
    "Bone Lesion": DiseaseInfo(
        name="Bone Lesion",
        description="A bone lesion is an abnormal area within the bone. Can be benign (bone cyst, enchondroma) or malignant (primary bone cancer or metastasis). Further imaging and possibly biopsy required.",
        common_symptoms=["Bone pain", "Swelling", "Pathologic fracture", "May be asymptomatic"],
        risk_category="high",
        specialist="Orthopedic Oncologist",
        icd10_code="M89.9"
    ),
}

# ============================================
# Combined Disease Database
# ============================================
ALL_DISEASES = {
    "chest_xray": CHEST_XRAY_DISEASES,
    "skin_image": SKIN_LESION_DISEASES,
    "bone_xray": BONE_XRAY_DISEASES,
}

# ============================================
# Recommendations by Risk Level
# ============================================
RECOMMENDATIONS = {
    "high": (
        "⚠️ URGENT MEDICAL ATTENTION REQUIRED\n\n"
        "This finding requires immediate evaluation by a medical professional. "
        "Please consult a specialist as soon as possible for proper diagnosis, "
        "additional testing, and treatment planning.\n\n"
        "DO NOT delay seeking medical care. Early intervention is crucial."
    ),
    "moderate": (
        "⚡ MEDICAL EVALUATION RECOMMENDED\n\n"
        "This finding warrants professional medical evaluation. "
        "Please schedule an appointment with a healthcare provider "
        "for further assessment and appropriate follow-up testing.\n\n"
        "While not immediately urgent, timely evaluation is important."
    ),
    "low": (
        "✓ ROUTINE MONITORING ADVISED\n\n"
        "This finding is likely benign but should be monitored. "
        "Continue with routine health check-ups and report any "
        "new symptoms or changes to your healthcare provider.\n\n"
        "Maintain a healthy lifestyle and follow screening guidelines."
    ),
    "normal": (
        "✓ NO SIGNIFICANT ABNORMALITIES\n\n"
        "The analysis did not detect any significant abnormalities. "
        "Continue routine health monitoring and maintain healthy habits.\n\n"
        "Remember: This AI analysis is for educational purposes only "
        "and does not replace professional medical evaluation."
    ),
}

# Specialist recommendations by image type
SPECIALISTS = {
    "chest_xray": {
        "high": "Pulmonologist, Oncologist, or Emergency Medicine Physician",
        "moderate": "Pulmonologist or Internal Medicine Physician",
        "low": "Primary Care Physician",
    },
    "skin_image": {
        "high": "Dermatologist or Dermatologic Oncologist",
        "moderate": "Dermatologist",
        "low": "Primary Care Physician or Dermatologist",
    },
    "bone_xray": {
        "high": "Orthopedic Surgeon or Orthopedic Oncologist",
        "moderate": "Orthopedic Specialist or Rheumatologist",
        "low": "Primary Care Physician",
    },
}


class DiseaseDatabase:
    """
    Medical Disease Database
    
    Provides comprehensive information about medical conditions
    detected by the AI models.
    """
    
    @classmethod
    def get_disease_info(cls, model_type: str, disease_name: str) -> DiseaseInfo:
        """Get detailed information about a disease"""
        diseases = ALL_DISEASES.get(model_type, {})
        
        if disease_name in diseases:
            return diseases[disease_name]
        
        # Return default info for unknown diseases
        return DiseaseInfo(
            name=disease_name,
            description=f"Medical condition detected: {disease_name}. Please consult a healthcare professional for detailed information.",
            common_symptoms=["Consult healthcare provider for symptoms"],
            risk_category="moderate",
            specialist="Healthcare Provider"
        )
    
    @classmethod
    def get_recommendation(cls, risk_level: str, model_type: str = None) -> str:
        """Get recommendation based on risk level"""
        base_recommendation = RECOMMENDATIONS.get(risk_level, RECOMMENDATIONS["moderate"])
        
        if model_type and risk_level in SPECIALISTS.get(model_type, {}):
            specialist = SPECIALISTS[model_type][risk_level]
            base_recommendation += f"\n\nRecommended Specialist: {specialist}"
        
        return base_recommendation
    
    @classmethod
    def get_specialist(cls, model_type: str, risk_level: str) -> str:
        """Get recommended specialist for condition"""
        return SPECIALISTS.get(model_type, {}).get(risk_level, "Healthcare Provider")
    
    @classmethod
    def get_all_diseases_by_type(cls) -> Dict[str, List[dict]]:
        """Get all diseases organized by image type"""
        result = {}
        for image_type, diseases in ALL_DISEASES.items():
            # Convert dataclass to dict with only the fields needed by the API schema
            result[image_type] = [
                {
                    "name": d.name,
                    "description": d.description,
                    "common_symptoms": d.common_symptoms
                }
                for d in diseases.values()
            ]
        return result
    
    @classmethod
    def get_disease_names(cls, model_type: str) -> List[str]:
        """Get list of disease names for a model type"""
        return list(ALL_DISEASES.get(model_type, {}).keys())
    
    @classmethod
    def format_findings_report(
        cls, 
        model_type: str,
        primary_finding: str,
        confidence: float,
        risk_level: str,
        all_findings: Dict[str, float] = None
    ) -> str:
        """Format a comprehensive findings report"""
        disease_info = cls.get_disease_info(model_type, primary_finding)
        
        report = f"""
═══════════════════════════════════════════════════════════
                    AI ANALYSIS REPORT
═══════════════════════════════════════════════════════════

PRIMARY FINDING: {primary_finding}
CONFIDENCE: {confidence*100:.1f}%
RISK LEVEL: {risk_level.upper()}

───────────────────────────────────────────────────────────
CONDITION DESCRIPTION:
───────────────────────────────────────────────────────────
{disease_info.description}

───────────────────────────────────────────────────────────
COMMON SYMPTOMS:
───────────────────────────────────────────────────────────
{chr(10).join(f"• {symptom}" for symptom in disease_info.common_symptoms)}

───────────────────────────────────────────────────────────
RECOMMENDATION:
───────────────────────────────────────────────────────────
{cls.get_recommendation(risk_level, model_type)}

═══════════════════════════════════════════════════════════
⚠️ DISCLAIMER: This AI analysis is for educational purposes 
only and does not constitute medical advice. Always consult 
a qualified healthcare professional for diagnosis and treatment.
═══════════════════════════════════════════════════════════
"""
        return report


# Global instance
disease_db = DiseaseDatabase()
