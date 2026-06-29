from fastapi import APIRouter, UploadFile, File, Form

from app.core.exceptions import BaseAppException, ValidationException
from app.core.logging import logger
from app.models.analysis_models import AnalysisResult
from app.services.file_service import FileService, FileType
from app.services.jd_parser import parse_jd_text
from app.services.llm_service import generate_analysis
from app.services.resume_parser import parse_resume_text
from app.services.scoring_service import calculate_skill_match
from app.utils.text_cleaner import clean_text
from app.utils.text_extraction import extract_text_from_docx, extract_text_from_pdf

router = APIRouter()


def decode_text_file(file_bytes: bytes) -> str:
    """Decode plain text resume content from bytes."""
    try:
        return file_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return file_bytes.decode("latin-1", errors="ignore")


@router.post("/analyze", response_model=AnalysisResult)
async def analyze_resume(
    resume_file: UploadFile = File(...),
    jd_text: str = Form(...),
):
    """Analyze a resume file against a provided job description."""
    try:
        file_bytes = await resume_file.read()
        filename = resume_file.filename

        is_valid, error_message = FileService.validate_file(
            filename=filename,
            file_size=len(file_bytes),
        )

        if not is_valid:
            logger.warning("Resume upload validation failed: %s", error_message)
            raise ValidationException(error_message)

        file_type = FileService.detect_file_type(filename)
        if file_type is None:
            raise ValidationException(
                f"Unsupported file type. Allowed types: {', '.join(FileService.ALLOWED_EXTENSIONS)}"
            )

        if file_type == FileType.PDF:
            resume_text = extract_text_from_pdf(file_bytes)
        elif file_type == FileType.DOCX:
            resume_text = extract_text_from_docx(file_bytes)
        elif file_type == FileType.TXT:
            resume_text = decode_text_file(file_bytes)
        else:
            raise ValidationException(
                f"Unsupported file type '{file_type.value}'."
            )

        cleaned_resume = clean_text(resume_text)
        cleaned_jd = clean_text(jd_text)

        resume_data = parse_resume_text(cleaned_resume)
        jd_data = parse_jd_text(cleaned_jd)

        skill_score = calculate_skill_match(resume_data.skills, jd_data.required_skills)
        analysis = generate_analysis(resume_data, jd_data, skill_score)

        return AnalysisResult(
            match_score=skill_score,
            strengths=analysis.get("strengths", []),
            missing_skills=analysis.get("missing_skills", []),
            recommendations=analysis.get("recommendations", []),
        )

    except BaseAppException:
        raise
    except Exception as exc:
        logger.exception("Error processing analyze request")
        raise BaseAppException("Failed to analyze resume") from exc
