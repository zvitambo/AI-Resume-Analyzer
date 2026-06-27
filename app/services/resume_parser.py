from app.models.resume_models import ResumeData


def extract_text_from_pdf(file_bytes) -> str:
    ...

def extract_text_from_docx(file_bytes) -> str:
    ...

def parse_resume_text(resume_text: str) -> ResumeData:
    ...