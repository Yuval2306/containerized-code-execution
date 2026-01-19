from flask import Flask, request, jsonify
import subprocess
import os
import tempfile

app = Flask(__name__)


@app.route('/execute', methods=['POST'])
def execute_dart():
    """Execute Dart code"""
    data = request.get_json()
    code = data.get('code')

    if not code:
        return jsonify({'error': 'No code provided'}), 400

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            dart_file = os.path.join(temp_dir, 'main.dart')
            with open(dart_file, 'w') as f:
                f.write(code)

            result = subprocess.run(['dart', dart_file],
                                    capture_output=True, text=True)

            return jsonify({'output': result.stdout, 'error': result.stderr})

    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
