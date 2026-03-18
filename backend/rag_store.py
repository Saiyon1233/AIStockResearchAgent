import faiss
import numpy as np
import google.genai as genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class RAGStore:
    def __init__(self):
        self.texts = []
        self.index = None

    # Text chunking method
    def chunk_text(self, text, chunk_size=800, overlap=100):
        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += chunk_size - overlap

        return chunks

    # Embedding method using Gemini API
    def embed(self, texts):
        BATCH_SIZE = 100
        all_embeddings = []

        # remove empty strings
        texts = [t for t in texts if t.strip()]

        for i in range(0, len(texts), BATCH_SIZE):
            batch = texts[i:i + BATCH_SIZE]

            print(f"Embedding batch {i//BATCH_SIZE + 1} ({len(batch)} items)")

            response = client.models.embed_content(
                model="gemini-embedding-001",
                contents=batch
            )

            batch_embeddings = [e.values for e in response.embeddings]
            all_embeddings.extend(batch_embeddings)

        return all_embeddings

    # Add documents to the RAG store
    def add_documents(self, texts):
        chunks = []
        for text in texts:
            if text not in self.texts:
                chunks.extend(self.chunk_text(text))
            
        if not chunks:
            return
        
        embeddings = self.embed(chunks)

        if self.index is None:
            dim = len(embeddings[0])
            self.index = faiss.IndexFlatL2(dim)

        self.index.add(np.array(embeddings).astype("float32"))
        self.texts.extend(chunks)

    # Retrieve relevant chunks based on a query
    def retrieve(self, query, k=3):
        if self.index is None or len(self.texts) == 0:
            return []

        query_embedding = self.embed([query])[0]

        D, I = self.index.search(
            np.array([query_embedding]).astype("float32"),
            k
        )

        return [self.texts[i] for i in I[0]]
    
# THIS IS A GLOBAL INSTANCE OF THE RAG STORE THAT CAN BE IMPORTED AND USED ACROSS MODULES
rag_store = RAGStore()

