from app.core.exceptions import LLMResponseError
from app.models.chat_model import LlamaChat, LangChainLlamaChat
from app.utils.json_parser import extract_json_from_response

# This is the single place that talks to the LLM provider.

# Responsibilities
# send prompts to the model
# receive responses
# enforce JSON output
# handle retries / parsing failures later

# The LLM converts raw text into structured JSON:

# name
# skills
# education
# experience 


llamaChat = LlamaChat()
langChainLlamaChat = LangChainLlamaChat()



def extract_resume_data(resume_text: str) -> dict:
    """Send resume text to the LLM and parse its structured JSON response.

    Args:
        resume_text: Raw text extracted from a resume document.

    Returns:
        Parsed resume data as a dictionary.
    """

    try:
        response = llamaChat.extract_resume_data_response(resume_text) 
        return extract_json_from_response(response)
    except Exception as e:
        raise LLMResponseError("failed to generate llm response while extracting resume data") from e
    
    

def extract_jd_data(jd_text: str) -> dict:
    """Send job description text to the LLM and parse its structured JSON response.

    Args:
        jd_text: Raw text extracted from a job description.

    Returns:
        Parsed job description data as a dictionary.
    """
    try:
        response = llamaChat.extract_jd_data_response(jd_text) 
        return extract_json_from_response(response)
    except Exception as e:
        raise LLMResponseError("failed to generate llm response while extracting job description data") from e
    
    

def generate_analysis(resume_data: dict, jd_data: dict, score: float) -> dict:
    """Generate an analysis summary from resume and job description data.

    Args:
        resume_data: Structured resume data.
        jd_data: Structured job description data.
        score: Initial match score to include as context.

    Returns:
        Parsed analysis result as a dictionary.
    """
    try:
        response = llamaChat.generate_analysis_prompt(resume_data, jd_data, score) 
        return extract_json_from_response(response)
    except Exception as e:
        raise LLMResponseError("failed to generate llm response while generating analysis") from e
    
    