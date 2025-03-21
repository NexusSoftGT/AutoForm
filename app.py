from flask import Flask, jsonify
import subprocess
from flask_cors import CORS


app = Flask(__name__)

CORS(app)


@app.route('/run-script', methods=['GET'])
def run_script():
    try:
        # Run the main.py script and capture its output
        result = subprocess.check_output(['python', 'main.py'], universal_newlines=True)
        return jsonify({"output": result})
    except Exception as e:
        # If there's an error, return it
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
