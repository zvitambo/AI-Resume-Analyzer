#    Purpose

# This is the orchestrator of the entire analysis workflow.

# This is one of the most important files in the project.
# Responsibilities

# It coordinates the full pipeline:

# receive uploaded resume + JD text
# call file_service
# call resume_parser
# call jd_parser
# call scoring_service
# call llm_service for final narrative analysis
# return final AnalysisResult
# Why it exists

# Without this file, your route would become a giant messy function doing everything.

# This service acts like the application workflow layer.





 #             Resume
    #                │
    #                ▼
    #       resume_parser.py
    #                │
    #       ResumeData object
    #                │
    #                ▼
    #         analyzer_service.py
    #                │
    #                │
    #     Job Description
    #                │
    #                ▼
    #         jd_parser.py
    #                │
    #          JobDescriptionData
    #                │
    #                ▼
    #      scoring_service.py
    #                │
    #   SkillMatchResult(score=78.5)
    #                │
    #                ▼
    #         llm_service.py
    #                │
    #                ▼
    #      Human-readable analysis
    #                │
    #                ▼
    #           API Response

    # resume_data = ...
    #     jd_data = ...
    #     score = ...
    #     analysis = ...
    #     return analysis



from app.core.exceptions import BaseAppException, InvalidFileTypeError
from app.services.file_service import FileService, FileType
from app.services.jd_parser import parse_jd_text
from app.services.llm_service import generate_analysis
from app.services.resume_parser import parse_resume_text
from app.services.scoring_service import calculate_skill_match, calculate_weighted_match
from app.utils.text_cleaner import clean_text
from app.utils.text_extraction import extract_text_from_docx, extract_text_from_pdf
from app.core.logging import logger



def analyze_resume(file: str, jd_text: str) -> None:

    resume_text = ""
    

    try:
        fileservice = FileService()

        if not fileservice.is_extension_allowed():
            raise InvalidFileTypeError("Unsupported file type")      
        

        file_type = fileservice.get_file_extension(file)

        file_bytes = fileservice.read_file_bytes(file)


        if file_type == FileType.PDF:
            resume_text = extract_text_from_pdf(file_bytes)
        elif file_type == FileType.DOCX:
            resume_text = extract_text_from_docx(file_bytes)
        
        cleaned_resume_text =clean_text(resume_text)
        cleaned_jde_text =clean_text(jd_text)

        resume_data = parse_resume_text(cleaned_resume_text)
        jd_data = parse_jd_text(cleaned_jde_text )

        calculate_skill_score = calculate_skill_match(resume_data.skills, jd_data.required_skills)
        #calculate_weighted_score = calculate_weighted_match(resume_data.skills, jd_data.required_skills, jd_data.preferred_skills)


        analysis = generate_analysis(resume_data, jd_data, calculate_skill_score)
       
        return analysis

        

    except Exception as e:
        logger.exception("error in analyze pipeline process ")
        raise BaseAppException("Internal database error") from e

    