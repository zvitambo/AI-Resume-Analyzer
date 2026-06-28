from app.models.resume_models import ResumeData
from app.services.llm_service import extract_resume_data
from app.utils.helpers import Dict2PydanticClass


    

def parse_resume_text(resume_text: str) -> ResumeData:
    resume_data_dict = extract_resume_data(resume_text)
    return Dict2PydanticClass(resume_data_dict, ResumeData)