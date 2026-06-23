AI Resume Analyzer
==================

Project Objective
-----------------
Build an AI-powered application that:

- Accepts a resume (PDF or DOCX)
- Extracts text from the resume
- Analyzes skills, education, and experience
- Compares the resume against a job description
- Generates a professional report including:
  - Match score
  - Missing skills
  - Strengths and weaknesses
  - Improvement suggestions

Core workflow
-------------
Document Upload → Document Processing → Information Extraction → LLM Analysis →
Prompt Engineering → API Development → Frontend Integration → Deployment

Features
--------

- Resume parsing (PDF/DOCX)
- Skill, education, and experience extraction
- Job-description matching and scoring
- Report generation (JSON / human-readable)
- Extensible prompt templates for LLM analysis

Repository structure
--------------------

- main.py — application entrypoint
- requirements.txt — Python dependencies
- [app](app/) — application package
  - [app/api](app/api/) — API routes and server code
  - [app/models](app/models/) — domain models (e.g., `DocumentModels.py`)
  - [app/prompts](app/prompts/) — prompt templates and prompt engineering helpers
  - [app/services](app/services/) — extraction and analysis services
  - [app/utils](app/utils/) — utility helpers
- data/ — sample documents, test fixtures, or datasets
- tests/ — unit and integration tests

Getting started
---------------

1. Clone the repository and navigate to the project root.

2. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# Windows cmd
.\.venv\Scripts\activate.bat
# macOS / Linux
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

Running the project
-------------------

Run the main entrypoint for quick local testing:

```bash
python main.py
```

If the project exposes an API in `app/api`, start the API server as documented in that folder (for example, a FastAPI or Flask `uvicorn`/`flask run` command).

Example usage
-------------

- Upload a resume (PDF/DOCX) to the appropriate API endpoint and provide a job description.
- The service will return a JSON report containing a match score, missing skills, and suggestions.

Testing
-------

Run tests with `pytest` from the project root:

```bash
pytest
```

Development notes
-----------------

- Text extraction: keep parsers isolated in `app/services` for PDF and DOCX.
- Prompt engineering: store templates in `app/prompts` and centralize LLM calls.
- Models: define serializable models in `app/models/DocumentModels.py`.

Contributing
------------

Contributions are welcome. Please open issues or pull requests describing changes.

License
-------

Include a license file if you want to make this project open source. If none is present, the repository is private by default.

Further improvements
--------------------

- Add CI (tests, linting) and pre-commit hooks
- Provide example API requests and a Postman/Insomnia collection
- Add Dockerfile and deployment instructions
