
from app.models.jd_models import JobDescriptionData

from app.services.llm_service import extract_jd_data
from app.utils.helpers import Dict2PydanticClass



def parse_jd_text(resume_text: str) -> JobDescriptionData:
    jd_data_dict = extract_jd_data(resume_text)
    return Dict2PydanticClass(jd_data_dict, JobDescriptionData)