from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

UPLOAD_FOLDER = '/tmp/uploads'

# Language executor URL
EXECUTORS = {
    'java': 'http://java-executor:5001/execute',
    'python': 'http://python-executor:5002/execute',
    'dart': 'http://dart-executor:5003/execute'
}


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle POST requests with code files """
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    language = request.form.get('language')

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not language:
        return jsonify({'error': 'Language not specified'}), 400

    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    return jsonify({'message': 'File uploaded successfully', 'filename': filename})


@app.route('/execute', methods=['GET'])
def execute_code():
    """Handle GET requests to execute code executor"""
    filename = request.args.get('filename')
    language = request.args.get('language')

    if not filename or not language:
        return jsonify({'error': 'Missing filename or language'}), 400

    filepath = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404

    with open(filepath, 'r') as f:
        code = f.read()

    if language not in EXECUTORS:
        return jsonify({'error': 'Unsupported language'}), 400

    try:
        response = requests.post(EXECUTORS[language], json={'code': code})
        return response.json()
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
