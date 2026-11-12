# CampusMate — Government Polytechnic Dwarahat

A clean, responsive college chatbot starter with branch/semester/subject filters and local PDF syllabus retrieval.

## Run on Windows
1. Install Python 3.10 or newer.
2. Extract this ZIP and open Command Prompt in the extracted folder.
3. Run `python -m venv .venv`
4. Run `.venv\\Scripts\\activate`
5. Run `pip install -r requirements.txt`
6. Copy `.env.example` to `.env` and add your OpenAI API key.
7. Copy official syllabus PDFs into the `knowledge` folder.
8. Run `python app.py` and open `http://127.0.0.1:5000`.

Keep your API key private. This prototype uses keyword-based PDF retrieval, not production-grade semantic search. Scanned PDFs may need OCR. Verify the branch options against the official college offerings before public launch.
