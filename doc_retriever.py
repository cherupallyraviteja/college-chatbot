from sentence_transformers import SentenceTransformer, util
from rank_bm25 import BM25Okapi

documents = []
corpus_tokens = []

embedder = SentenceTransformer("all-MiniLM-L6-v2")

def load_docs(text_list):
    global documents, corpus_tokens
    documents = text_list
    corpus_tokens = [doc.lower().split() for doc in documents]

def retrieve(query, top_k=3):
    bm25 = BM25Okapi(corpus_tokens)
    scores = bm25.get_scores(query.lower().split())
    top_idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
    return [documents[i] for i in top_idx]
