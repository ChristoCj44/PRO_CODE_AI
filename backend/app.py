from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os

from backend.executor.runner import CodeRunner
from backend.complexity.analyzer import ComplexityAnalyzer

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "../frontend")

app = Flask(
    __name__,
    static_folder=FRONTEND_DIR,
    static_url_path=""
)

CORS(app)

runner = CodeRunner()
analyzer = ComplexityAnalyzer()


# ✅ Homepage
@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


# ✅ API
@app.route("/api/execute", methods=["POST"])
def execute_code():
    try:
        data = request.get_json()
        language = data.get("language", "python")
        code = data.get("code")

        if not code:
            return jsonify({"error": "Missing code"}), 400

        exec_result = runner.run(language, code)
        complexity_result = analyzer.analyze(language, code)

        return jsonify({
            "output": exec_result.get("output", ""),
            "error": exec_result.get("error", ""),
            "execution_time": exec_result.get("execution_time", 0),
            "complexity": complexity_result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
