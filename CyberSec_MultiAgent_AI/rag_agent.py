from pathlib import Path
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class RAGAgent:
    """Local document retrieval agent. Uses TF-IDF so it can run without an embedding API."""

    def __init__(self):
        self.chunks = []
        self.vectorizer = None
        self.matrix = None
        self.source = None

    def load_file(self, path):
        path = Path(path)
        self.source = path.name
        if path.suffix.lower() == ".pdf":
            reader = PdfReader(str(path))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        else:
            text = path.read_text(encoding="utf-8", errors="ignore")

        words = text.split()
        size = 180
        overlap = 30
        self.chunks = []
        for i in range(0, len(words), size - overlap):
            chunk = " ".join(words[i:i+size])
            if chunk.strip():
                self.chunks.append(chunk)
        if not self.chunks:
            self.chunks = [text[:5000]]

        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.matrix = self.vectorizer.fit_transform(self.chunks)
        return len(self.chunks)

    def retrieve(self, query, k=4):
        if not self.chunks:
            return []
        q = self.vectorizer.transform([query])
        scores = cosine_similarity(q, self.matrix)[0]
        idx = scores.argsort()[::-1][:k]
        return [{"text": self.chunks[i], "score": float(scores[i]), "rank": n+1}
                for n, i in enumerate(idx)]

    def answer(self, query, llm):
        hits = self.retrieve(query)
        context = "\n\n".join(
            f"[Chunk {h['rank']}] {h['text']}" for h in hits
        )
        prompt = f"""Answer the user's question using ONLY the retrieved document context.
If the context does not contain the answer, say that clearly.
Question: {query}

Retrieved context:
{context}
"""
        return llm(prompt), hits
