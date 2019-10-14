from flask import Flask, jsonify, request
from teams import teams

app = Flask(__name__)
app.register_blueprint(teams)

@app.route('/api', methods=['POST', 'DELETE', 'GET'])
def my_microservice():
    print(request)
    response = jsonify({'Hello': 'World'})
    print(response)
    print(response.data)
    return response


@app.route('/api/person/<person_id>')
def person(person_id):
    response = jsonify({'Hello': person_id})
    return response


if __name__ == '__main__':
    app.run(debug=True)
