from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

ROUTER_URL = 'http://router:5000'

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Code Execution System</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f7fa;
            color: #333;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2.2em;
        }
        h2 {
            color: #34495e;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            margin-top: 30px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #555;
        }
        select, input[type="file"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 6px;
            font-size: 16px;
            box-sizing: border-box;
            transition: border-color 0.3s;
        }
        select:focus, input[type="file"]:focus {
            outline: none;
            border-color: #3498db;
        }
        .upload-btn {
            background: linear-gradient(45deg, #3498db, #2980b9);
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.3s;
            margin-top: 10px;
        }
        .upload-btn:hover {
            background: linear-gradient(45deg, #2980b9, #1f4e79);
        }
        .result-box {
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 6px;
            padding: 20px;
            margin-top: 20px;
            font-family: 'Courier New', monospace;
            white-space: pre-wrap;
            max-height: 400px;
            overflow-y: auto;
        }
        .result-success {
            border-left: 4px solid #27ae60;
            background-color: #d5f4e6;
        }
        .result-error {
            border-left: 4px solid #e74c3c;
            background-color: #fadbd8;
            color: #c0392b;
        }
        .language-info {
            background: #ecf0f1;
            padding: 15px;
            border-radius: 6px;
            margin-top: 20px;
        }
        .language-info h3 {
            margin-top: 0;
            color: #2c3e50;
        }
        .lang-item {
            display: inline-block;
            background: #3498db;
            color: white;
            padding: 5px 12px;
            margin: 5px;
            border-radius: 15px;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Multi-Language Code Execution System</h1>

        <h2>Upload and Execute Code</h2>
        <form method="POST" action="/upload" enctype="multipart/form-data">
            <div class="form-group">
                <label for="language">Select Programming Language:</label>
                <select name="language" id="language" required>
                    <option value="">Choose language...</option>
                    <option value="java"> Java</option>
                    <option value="python"> Python</option>
                    <option value="dart"> Dart</option>
                </select>
            </div>

            <div class="form-group">
                <label for="file">Upload Code File:</label>
                <input type="file" name="file" id="file" required>
            </div>

            <button type="submit" class="upload-btn">▶️ Upload and Execute</button>
        </form>

        {% if result %}
        <h2>✅ Execution Result:</h2>
        <div class="result-box result-success">{{ result }}</div>
        {% endif %}

        {% if error %}
        <h2>❌ Error:</h2>
        <div class="result-box result-error">{{ error }}</div>
        {% endif %}

        <div class="language-info">
            <h3>🎯 Supported Languages:</h3>
            <span class="lang-item">Java (.java)</span>
            <span class="lang-item">Python (.py)</span>
            <span class="lang-item">Dart (.dart)</span>
        </div>
    </div>
</body>
</html>
'''


@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        file = request.files['file']
        language = request.form['language']

        if not file or file.filename == '':
            return render_template_string(HTML_TEMPLATE, error="No file selected")

        files = {'file': (file.filename, file.read(), file.content_type)}
        data = {'language': language}

        upload_response = requests.post(f'{ROUTER_URL}/upload', files=files, data=data)

        if upload_response.status_code != 200:
            error = upload_response.json().get('error', 'Upload failed')
            return render_template_string(HTML_TEMPLATE, error=error)

        upload_result = upload_response.json()
        actual_filename = upload_result['filename']

        execute_response = requests.get(f'{ROUTER_URL}/execute',
                                        params={'filename': actual_filename, 'language': language})

        if execute_response.status_code != 200:
            return render_template_string(HTML_TEMPLATE, error="Execution failed")

        result_data = execute_response.json()

        if 'error' in result_data and result_data['error']:
            return render_template_string(HTML_TEMPLATE, error=result_data['error'])
        else:
            output = result_data.get('output', '').strip()
            error_output = result_data.get('error', '').strip()

            if output:
                result = f"Output:\n{output}"
                if error_output:
                    result += f"\n\nWarnings/Errors:\n{error_output}"
            elif error_output:
                result = f"Errors:\n{error_output}"
            else:
                result = "Code executed successfully (no output)"

            return render_template_string(HTML_TEMPLATE, result=result)

    except Exception as e:
        return render_template_string(HTML_TEMPLATE, error=f"System error: {str(e)}")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)