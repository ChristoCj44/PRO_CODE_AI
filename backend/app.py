from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from backend.executor.runner import CodeRunner
from backend.complexity.analyzer import ComplexityAnalyzer

load_dotenv()

app = Flask(__name__)
CORS(app)

runner = CodeRunner()
analyzer = ComplexityAnalyzer()


@app.route('/api/execute', methods=['POST'])
def execute_code():
    try:
        data = request.get_json()
        language = data.get('language', 'python')
        code = data.get('code')

        if not code:
            return jsonify({'error': 'Missing code'}), 400

        exec_result = runner.run(language, code)
        complexity_result = analyzer.analyze(language, code)

        return jsonify({
            'output': exec_result.get('output', ''),
            'error': exec_result.get('error', ''),
            'execution_time': exec_result.get('execution_time', 0),
            'complexity': complexity_result
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# IMPORTANT: do NOT run app.run() on Vercel
