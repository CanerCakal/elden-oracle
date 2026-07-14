from foundry_local_sdk import Configuration, FoundryLocalManager
from retrieval import get_top_chunks

CHAT_MODEL = "phi-3.5-mini"

SYSTEM_PROMPT = """You are Elden Oracle, an expert assistant on the lore of Elden Ring.

Answer the user's question using ONLY the context provided below.
Do not use any outside knowledge. Do not invent facts.
If the context does not contain the answer, reply exactly:
"I don't have that information in my records."

Keep your answer clear and concise."""

_model = None


def get_chat_model():
    global _model
    if _model is None:
        config = Configuration(app_name="elden-oracle")
        FoundryLocalManager.initialize(config)
        manager = FoundryLocalManager.instance
        model = manager.catalog.get_model(CHAT_MODEL)
        model.download()
        model.load()
        _model = model
    return _model


def build_context(results):
    blocks = []
    for score, chunk in results:
        blocks.append(f"[Source: {chunk['source']}]\n{chunk['text']}")
    return "\n\n".join(blocks)


def answer_query(question, top_k=5):
    results = get_top_chunks(question, top_k=top_k)
    context = build_context(results)

    user_message = f"Context:\n{context}\n\nQuestion: {question}"

    model = get_chat_model()
    client = model.get_chat_client()
    response = client.complete_chat([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message}
    ])

    answer = response.choices[0].message.content

    sources = []
    for score, chunk in results:
        if chunk["source"] not in sources:
            sources.append(chunk["source"])

    retrieved = []
    for score, chunk in results:
        retrieved.append({
            "source": chunk["source"],
            "score": round(float(score), 3),
            "text": chunk["text"]
        })

    return answer, sources, retrieved

def answer_without_rag(question):
    model = get_chat_model()
    client = model.get_chat_client()
    response = client.complete_chat([
        {"role": "system", "content": "You are an assistant answering questions about Elden Ring lore."},
        {"role": "user", "content": question}
    ])
    return response.choices[0].message.content

if __name__ == "__main__":
    question = "What is Radagon's secret?"
    print(f"Question: {question}\n")
    answer, sources, retrieved = answer_query(question)
    print("Answer:")
    print(answer)
    print(f"\nSources: {', '.join(sources)}")
    print(f"\nRetrieved {len(retrieved)} chunks:")
    for r in retrieved:
        print(f"  [{r['score']}] {r['source']}")