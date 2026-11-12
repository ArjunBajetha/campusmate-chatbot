import re
from pathlib import Path
KNOWLEDGE_DIR = Path(__file__).parent / 'knowledge'
CHUNK_SIZE, OVERLAP = 1000, 150

def _read_pdfs():
    try:
        from pypdf import PdfReader
    except ImportError:
        return []
    docs = []
    for path in KNOWLEDGE_DIR.glob('*.pdf'):
        try:
            for page_num, page in enumerate(PdfReader(str(path)).pages, 1):
                text = re.sub(r'\s+', ' ', page.extract_text() or '').strip()
                start = 0
                while start < len(text):
                    chunk = text[start:start + CHUNK_SIZE]
                    if chunk.strip(): docs.append({'text': chunk, 'source': path.name, 'page': page_num})
                    start += CHUNK_SIZE - OVERLAP
        except Exception:
            continue
    return docs

def retrieve_context(question, branch='', semester='', subject=''):
    docs = _read_pdfs()
    if not docs: return '', []
    qterms = set(re.findall(r'[a-zA-Z0-9]+', question.lower()))
    filters = set(re.findall(r'[a-zA-Z0-9]+', ' '.join([branch, semester, subject]).lower()))
    scored = []
    for doc in docs:
        hay = doc['text'].lower()
        score = sum(1 for t in qterms if len(t) > 2 and t in hay)
        score += 2 * sum(1 for t in filters if len(t) > 2 and t in hay)
        if score: scored.append((score, doc))
    scored.sort(key=lambda x: x[0], reverse=True)
    passages, sources = [], []
    for _, doc in scored[:4]:
        passages.append(f"[Source: {doc['source']}, page {doc['page']}]\n{doc['text']}")
        item = {'file': doc['source'], 'page': doc['page']}
        if item not in sources: sources.append(item)
    return '\n\n'.join(passages), sources
