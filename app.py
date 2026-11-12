import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from knowledge import retrieve_context
load_dotenv()
app = Flask(__name__)

@app.get('/')
def home():
    return render_template('index.html')

@app.post('/api/chat')
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get('message') or '').strip()
    branch = (data.get('branch') or '').strip()
    semester = (data.get('semester') or '').strip()
    subject = (data.get('subject') or '').strip()
    if not message:
        return jsonify({'answer': 'Type a question first.'}), 400
    context, sources = retrieve_context(message, branch, semester, subject)
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        return jsonify({'answer': 'The interface is ready, but AI is not connected yet. Add your OpenAI API key to the .env file and put official syllabus PDFs in the knowledge folder.', 'sources': sources, 'setup_required': True})
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        prompt = f'''You are the academic assistant for Government Polytechnic Dwarahat. Answer in clear, student-friendly language. Use the syllabus excerpts for syllabus-specific claims. Never invent college rules, dates, fees, or syllabus details. If the documents do not support an answer, say so. General educational explanations are allowed, but distinguish them from official syllabus facts.\nSelected branch: {branch or 'not selected'}\nSelected semester: {semester or 'not selected'}\nSelected subject: {subject or 'not selected'}\nSyllabus excerpts:\n{context or 'No relevant syllabus text was retrieved.'}\nStudent question: {message}'''
        response = client.responses.create(model=os.getenv('OPENAI_MODEL', 'gpt-4.1-mini'), input=prompt)
        return jsonify({'answer': response.output_text, 'sources': sources})
    except Exception:
        app.logger.exception('Chat request failed')
        return jsonify({'answer': "I couldn't generate an answer. Check your API key, internet connection, and server logs.", 'sources': sources}), 500

if __name__ == '__main__':
    app.run(debug=True)
