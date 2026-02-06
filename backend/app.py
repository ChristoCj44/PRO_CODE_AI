from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from dotenv import load_dotenv
from executor.runner import CodeRunner
from complexity.analyzer import ComplexityAnalyzer

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# Initialize modules
runner = CodeRunner()
analyzer = ComplexityAnalyzer()

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/execute', methods=['POST'])
def execute_code():
    data = request.json
    language = data.get('language', 'python') # Default to python
    code = data.get('code')

    if not code:
        return jsonify({'error': 'Missing code'}), 400

    # 1. Execute Code
    exec_result = runner.run(language, code)

    # 2. Analyze Complexity (AI)
    complexity_result = analyzer.analyze(language, code)

    response = {
        'output': exec_result.get('output', ''),
        'error': exec_result.get('error', ''),
        'execution_time': exec_result.get('execution_time', 0),
        'complexity': complexity_result
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
