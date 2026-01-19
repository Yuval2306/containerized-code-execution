from flask import Flask, request, jsonify
import subprocess
import os
import tempfile

app = Flask(__name__)


@app.route('/execute', methods=['POST'])
def execute_java():
    """Execute Java code"""
    data = request.get_json()
    code = data.get('code')

    if not code:
        return jsonify({'error': 'No code provided'}), 400

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            java_file = os.path.join(temp_dir, 'Main.java')
            with open(java_file, 'w') as f:
                f.write(code)

            compile_result = subprocess.run(['javac', java_file],
                                            capture_output=True, text=True)

            if compile_result.returncode != 0:
                return jsonify({'error': compile_result.stderr})

            run_result = subprocess.run(['java', '-cp', temp_dir, 'Main'],
                                        capture_output=True, text=True)

            return jsonify({'output': run_result.stdout, 'error': run_result.stderr})

    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)