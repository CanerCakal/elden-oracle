from flask import Flask, request, jsonify, send_from_directory, Response, stream_with_context
from rag import (
    answer_query,
    answer_without_rag,
    stream_answer_query,
    stream_answer_without_rag,
)
import json

app = Flask(__name__)


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "").strip()
    use_rag = data.get("use_rag", True)

    if not question:
        return jsonify({"error": "Question is empty."}), 400

    if use_rag:
        answer, sources, retrieved = answer_query(question)
        return jsonify({
            "answer": answer,
            "sources": sources,
            "retrieved": retrieved
        })
    else:
        answer = answer_without_rag(question)
        return jsonify({"answer": answer, "sources": []})
    

@app.route("/compare", methods=["POST"])
def compare():
    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "Question is empty."}), 400

    rag_answer, sources, retrieved = answer_query(question)
    plain_answer = answer_without_rag(question)

    return jsonify({
        "rag": {
            "answer": rag_answer,
            "sources": sources,
            "retrieved": retrieved
        },
        "plain": {
            "answer": plain_answer
        }
    })
    

@app.route("/ask-stream", methods=["POST"])
def ask_stream():
    data = request.get_json()
    question = data.get("question", "").strip()
    use_rag = data.get("use_rag", True)

    if not question:
        return jsonify({"error": "Question is empty."}), 400

    if use_rag:
        token_stream, sources, retrieved = stream_answer_query(question)
        meta = {"sources": sources, "retrieved": retrieved}
    else:
        token_stream = stream_answer_without_rag(question)
        meta = {"sources": [], "retrieved": []}

    def generate():
        yield json.dumps({"type": "meta", "data": meta}) + "\n"
        for token in token_stream():
            yield json.dumps({"type": "token", "data": token}) + "\n"
        yield json.dumps({"type": "done"}) + "\n"

    return Response(
        stream_with_context(generate()),
        mimetype="application/x-ndjson"
    )

if __name__ == "__main__":
    app.run(port=5000, debug=True)