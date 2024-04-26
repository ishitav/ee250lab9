from flask import Flask, request, jsonify
from main import process1, process2  # Assuming process2 is imported as well.

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'message': 'Welcome'})

@app.route('/process1', methods=['POST'])
def process1_route():
    """Process the data using process1."""
    data = request.get_json()
    return jsonify(process1(data))

@app.route('/process2', methods=['POST'])
def process2_route():
    """Process the data using process2."""
    data = request.get_json()
    return jsonify(process2(data))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
