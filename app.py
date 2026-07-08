from flask import Flask, request, jsonify, send_from_directory
from rag import answer_query, answer_without_rag

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
        answer, sources = answer_query(question)
        return jsonify({"answer": answer, "sources": sources})
    else:
        answer = answer_without_rag(question)
        return jsonify({"answer": answer, "sources": []})


if __name__ == "__main__":
    app.run(port=5000, debug=True)