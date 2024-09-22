from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/add', methods=['POST'])
def add_numbers():
    data = request.get_json()
    num1 = data.get('num1')
    num2 = data.get('num2')
    if num1 is None or num2 is None:
        return jsonify({"error": "Both num1 and num2 are required"}), 400
    
    try:
        result = float(num1) + float(num2)
        return jsonify({"sum": result}), 200
    except ValueError:
        return jsonify({"error": "Invalid input, please provide numeric values"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)