# 🚀 Multi-Language Code Execution System

A Docker-based microservices system for executing code in programming languages : Java, Python, Dart, 
using Flask web framework.

## 📁 Project Structure

```
code-execution-system/
├── docker-compose.yml          # Orchestrates all containers
├── router/                     # Main routing service
│   ├── app.py                 # Flask router (POST/GET endpoints)
│   ├── Dockerfile             # Alpine Linux + Python + Flask
│   └── requirements.txt       # Python dependencies
├── java-executor/             # Java code execution service
│   ├── app.py                 # Flask app for Java execution
│   ├── Dockerfile             # Alpine Linux + OpenJDK + Flask
│   └── requirements.txt       # Python dependencies
├── python-executor/           # Python code execution service
│   ├── app.py                 # Flask app for Python execution
│   ├── Dockerfile             # Alpine Linux + Python + Flask
│   └── requirements.txt       # Python dependencies
├── dart-executor/             # Dart code execution service
│   ├── app.py                 # Flask app for Dart execution
│   ├── Dockerfile             # Alpine Linux + Dart SDK + Flask
│   └── requirements.txt       # Python dependencies
├── client/                    # Web interface
│   ├── app.py                 # Flask web client with UI
│   ├── Dockerfile             # Alpine Linux + Python + Flask
│   └── requirements.txt       # Python dependencies
└── test-files/                # Sample code files
    ├── Main.java              # Java hello world
    ├── script.py              # Python hello world
    └── main.dart              # Dart hello world
```

## 🏗️ Architecture

### System Flow:
1. **Client** → Upload code file via web interface
2. **Router** → Receives file (POST), saves to temp directory
3. **Router** → Reads file (GET), forwards to appropriate executor
4. **Executor** → Runs code in sandboxed environment
5. **Client** → Displays execution results

### Container Communication:
- **router**: `http://router:5000`
- **java-executor**: `http://java-executor:5001`
- **python-executor**: `http://python-executor:5002`
- **dart-executor**: `http://dart-executor:5003`
- **client**: `http://client:5004`
