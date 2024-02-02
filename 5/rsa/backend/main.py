from flask import Flask, request
import json
from application import Application
from functools import reduce
import random

app = Flask(__name__)

def gener_simple_number(bits):
    num = 1
    stepen = 1
    for i in range(0, bits - 1):
        rand = random.randint(0, 1000000)
        if(rand % 2 == 1): num += 2**stepen
        stepen += 1
    return num

def is_prime(n, k):
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    
    # Представим n-1 в виде (2^r) * s
    # n - 1 = четное, s - остаток, r - степени двойки
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    
    # Повторить k раз
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, s, n)
        
        if x == 1 or x == n - 1:
            continue
        
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    
    return True

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def find_e(p, q):
    phi_n = (p - 1) * (q - 1)
    while True:
        e = random.randrange(2, phi_n//3)
        if gcd(e, phi_n) == 1 and is_prime(e, k = 5):
            # print('мое число')
            # print(e)
            return e

# расширенный алго евклида
# возвращает НОД(a, b), и коэффициенты x, y
def euclid(a, b):
    if a == 0:
        return (b, 0, 1)
    
    d, x, y = euclid(b % a, a)
    x1 = y - (b // a) * x
    y1 = x
    return (d, x1, y1)


@app.route('/gener', methods=['POST'])
def gener():
    # res = json.loads(request.get_data())
    # bits = int(res['bits'])
    bits = 16

    p = gener_simple_number(bits)
    q = gener_simple_number(bits)

    while is_prime(p, bits) == False: 
        p = gener_simple_number(bits)

    while is_prime(q, bits) == False: 
        q = gener_simple_number(bits)

    N = p * q
    fiN = (p - 1)*(q - 1)
    e = find_e(p, q)

    d, x, y = euclid(e, fiN)
    if d != 1:
        raise ValueError()
    else:
        x = (x % fiN + fiN) % fiN

    print(p)
    print(q)
    print(N)
    print(fiN)
    print(e)
    print(x)    

    # if((e * x) % fiN == 1): print('okey')
    # else: print('ну ты чего')

    # return json.dumps({'status': 'ok', 'result': {"p": str(p), "q": str(q), "N": str(N), "fiN": str(fiN), "e": str(e), "d": str(x)}})


def fast_power(base, exponent, n):
    result = 1
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % n
        base = (base * base) % n
        exponent //= 2
    return result

def convert_text_to_numbers(text):
    return [ord(char) for char in text]

def encrypt(message, e, n):
    numbers = convert_text_to_numbers(message)
    encrypted_blocks = [str(fast_power(num, e, n)) for num in numbers]
    encrypted_message = ' '.join(encrypted_blocks)
    return encrypted_message

@app.route('/cipher',methods=["POST"])
def test():
    res = json.loads(request.get_data())
    e = res['e']
    N = res['N']
    text = res["text"]
    e = int(e)
    N = int(N)

    message = encrypt(text, e, N)
    
    return json.dumps({'status': 'ok', 'text': message})

def convert_numbers_to_text(numbers):
    return ''.join([chr(num) for num in numbers])

def decrypt(ciphertext, d, n):
    try:
        encrypted_blocks = ciphertext.split()
        numbers = [fast_power(int(block), d, n) for block in encrypted_blocks]
        decrypted_message = convert_numbers_to_text(numbers)
        return decrypted_message
    except:
        return 'error'

@app.route('/decipher',methods=["POST"])
def decipher():
    res = json.loads(request.get_data())
    d = res['d']
    N = res['N']
    d = int(d)
    N = int(N)
    print(d)
    print(N)

    text = res["text"]

    message = decrypt(text, d, N)
    if(message == 'error'):
        return json.dumps({'status': 'ok', 'error': 'error'})
    return json.dumps({'status': 'ok', 'text': message})

if __name__ == '__main__':
    # app.run(debug=True, host="localhost", port='5000')
    gener()
