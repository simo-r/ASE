def sign(n):
    result = 1
    if n < 0:
        result = -1
    return result

def sum(m, n):
    added_value = sign(n)
    for x in range(abs(n)):
        m += added_value
    return m

def subtract(m,n):
    return sum(m,-1*n)

def divide(m, n):
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
    return result * n_sign * m_sign

def multiply(m,n):
    sum_value = abs(n)
    m_sign = sign(m)
    n_sign = sign(n)
    for x in range(n):
        m +=sum_value
    return m * m_sign * n_sign

print(divide(3, -3))
print(sum(3, 4))
print(subtract(2,3))