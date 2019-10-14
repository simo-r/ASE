from flakon import JsonBlueprint
from flask import Flask, request, jsonify

calc = JsonBlueprint('calc', __name__)

#IMPLEMENT OTHER METHODS

def sign(n):
    result = 1
    if n < 0:
        result = -1
    return result

@calc.route('/calc/sum', methods=['GET'])
def sum():
    # http://127.0.0.1:500/calc/sum?m=3&n=5
    m = int(request.args.get('m'))
    n = int(request.args.get('n'))
    print(m)
    print(n)
    added_value = sign(n)
    for x in range(abs(n)):
        m += added_value

    return jsonify({'result': str(m)})

@calc.route('/calc/sub', methods=['GET'])
def subtract():
    m = int(request.args.get('m'))
    n = int(request.args.get('n'))
    return jsonify({'result': str(sum(m,-1*n))})


@calc.route('/calc/div', methods=['GET'])
def divide():
    m = int(request.args.get('m'))
    n = int(request.args.get('n'))
    subtract_value = abs(n)
    initial_value = abs(m)
    m_sign = sign(m)
    n_sign = sign(n)
    result = 0
    while initial_value > 0:
        initial_value -= subtract_value
        result += 1
    if initial_value < 0:
        result -= 1
    return jsonify({'result': str(result * n_sign * m_sign)})


@calc.route('/calc/mul', methods=['GET'])
def multiply():
    m = int(request.args.get('m'))
    n = int(request.args.get('n'))
    sum_value = abs(n)
    m_sign = sign(m)
    n_sign = sign(n)
    for x in range(n):
        m +=sum_value
    return jsonify({'result': str(m * m_sign * n_sign)})
