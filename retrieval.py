import numpy as np
from embeddings import embed_text
from database import get_all_chunks


def cosine_similarity(vec_a, vec_b):
    a = np.array(vec_a)
    b = np.array(vec_b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def get_top_chunks(query, top_k=3):
    query_vector = embed_text(query)
    chunks = get_all_chunks()

    scored = []
    for chunk in chunks:
        score = cosine_similarity(query_vector, chunk["embedding"])
        scored.append((score, chunk))

    scored.sort(key=lambda item: item[0], reverse=True)

    return scored[:top_k]


if __name__ == "__main__":
    query = "What did Ranni do to her own body?"
    results = get_top_chunks(query)

    print(f"Soru: {query}\n")
    for score, chunk in results:
        print(f"[Skor: {score:.3f}] Kaynak: {chunk['source']}")
        print(chunk["text"][:200], "...\n")