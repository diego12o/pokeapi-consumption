from flask import Flask, jsonify, json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_solution():
    response = {} 
    with open('solution.json', 'r') as file:
        content = file.read()
        response = json.loads(content)

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='localhost', port=5000)