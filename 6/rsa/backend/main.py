from flask import Flask, request
import json
from application import Application
from functools import reduce
from itertools import chain
import random
from math import sqrt

app = Flask(__name__)

def gener_simple_number(bits):
    num = 1
    stepen = 1
    for i in range(0, bits - 1):
        rand = random.randint(0, 1000000)
        if(rand % 2 == 1): num += 2**stepen
        stepen += 1
    return num

def is_prime(n, k = 10):
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
            print(e)
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
    res = json.loads(request.get_data())
    bits = int(res['bits'])

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

    print('p: ' + str(p))
    print('q: ' + str(q))
    print('N: ' + str(N))
    print('fiN: ' + str(fiN))
    print('e: ' + str(e))
    print('d: ' + str(x))  

    if((e * x) % fiN == 1): print('okey')
    else: print('ну ты чего')

    return json.dumps({'status': 'ok', 'result': {"p": str(p), "q": str(q), "N": str(N), "fiN": str(fiN), "e": str(e), "d": str(x)}})


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

def isqrt(n):
    l, r = 1, n
    while r - l > 1:
        tm = (l + r) // 2
        if tm * tm > n:
            r = tm
        else:
            l = tm

    if l * l == n:
        return l
    if r * r == n:
        return r
    
    return None

# символ Лежандра
def legendre(a, p):
    return fast_power(a, (p - 1) // 2, p)

# решето Эратосфена, генерирует список простых чисел, которые <= n
# например, при n = 10 результат будет
# [2, 3, 5, 7]
def prime_gen(n):
    if n < 2:
        return list()

    isPrime = list(True for i in range(n+1))

    isPrime[0]=False
    isPrime[1]=False

    for j in range(2, int(n/2)): # проходимся по всем числам
        if isPrime[j]:
            for i in range(2*j, n+1, j): # убираем все числа деляющиеся на число j 
                isPrime[i] = False

    primes = list()
    for i in range(0, n+1):
        if isPrime[i]:
            primes.append(i) # добавляем все простые числа
            
    return primes

# генерирует факторную базу из B-гладких чисел
def find_base(N,B):

    factor_base = []
    primes = prime_gen(B)
    
    for p in primes:
        if legendre(N,p) == 1: # символ лежандро этого числа единица
            # в факторную базу заносятся только те простые числа, которые
            # являются квадратичным вычетом по модулю p
            factor_base.append(p)
    return factor_base

# транспонирует матрицу
def transpose(matrix):
    new_matrix = []
    for i in range(len(matrix[0])):
        new_row = []
        for row in matrix:
            new_row.append(row[i])
        new_matrix.append(new_row)
    return(new_matrix)

# строим матрицу из единиц и нулей (как в примере в методичке)
def build_matrix(smooth_nums,factor_base):

    # функция для факторизации числа, то есть находит список всех простых делителей
    # из факторной базы
    # например, для n = 12 результат будет
    # [2, 2, 3]
    def factor(n,factor_base):
        factors = []
        if n < 0:
            factors.append(-1)
        for p in factor_base:
            if p == -1:
                pass
            else:
                while n % p == 0:
                    factors.append(p)
                    n //= p
        return factors

    # результирующая матрица, которая будет из 0 и 1
    M = []
    # расширяем факторную базу на всякий случай
    factor_base.insert(0,-1)

    for n in smooth_nums:
        # вектор, в котором будут записаны количества простых делителей n
        # например, если n = 12 и факторная база [2, 3, 5, 7]
        # то exp_vector = [0, 1, 0, 0]
        # то есть [2 % 2, 1 % 2, 0 % 2, 0 % 2]
        # поскольку 12 дважды делится на 2 и один раз делится на 3
        exp_vector = [0]*(len(factor_base))
        n_factors = factor(n,factor_base)
        for i in range(len(factor_base)):
            if factor_base[i] in n_factors:
                exp_vector[i] = (exp_vector[i] + n_factors.count(factor_base[i])) % 2

        # если нашли какую-то строку только из нулей
        # значит, наше гладкое число подходит
        if 1 not in exp_vector:
            return True, n
        else:
            pass
        
        M.append(exp_vector)

    return (False, transpose(M))

# функция для решения уравнения (x*x) % p == N % p
# алгоритм Тонелли-Шэнкса
def tonelli(n, p):
    assert legendre(n, p) == 1, "not a square (mod p)"
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    if s == 1:
        r = fast_power(n, (p + 1) // 4, p)
        return r,p-r
    for z in range(2, p):
        if p - 1 == legendre(z, p):
            break
    c = fast_power(z, q, p)
    r = fast_power(n, (q + 1) // 2, p)
    t = fast_power(n, q, p)
    m = s
    t2 = 0
    while (t - 1) % p != 0:
        t2 = (t * t) % p
        for i in range(1, m):
            if (t2 - 1) % p == 0:
                break
            t2 = (t2 * t2) % p
        b = fast_power(c, 1 << (m - i - 1), p)
        r = (r * b) % p
        c = (b * b) % p
        t = (t * c) % p
        m = i

    return (r,p-r)

# поиск B-гладких чисел
def find_smooth1(factor_base,N,I):

    # генерируем массив из чисел (x^2 - n) на отрезке [sqrt(N) - I, sqrt(N) + I]
    def sieve_prep(N,I):
        root = int(sqrt(N))
        return list(x**2 - N for x in range(root-I,root+I))
    
    sieve_seq = sieve_prep(N,I)
    sieve_list = sieve_seq.copy()
    
    factor_base_begin_ind = 0
    # если первое простое число - 2, то делаем отдельно
    if factor_base[0] == 2:
        factor_base_begin_ind = 1

        # делим каждое число на наше простое, пока делится
        for j in range(0,len(sieve_list)):
            while sieve_list[j] % 2 == 0:
                sieve_list[j] //= 2
        

    root = int(sqrt(N))
    for p in factor_base[factor_base_begin_ind:]:

        # просто делим каждое число на простой делитель, пока делится
        for i in range(len(sieve_list)):
            while sieve_list[i] % p == 0:
                sieve_list[i] //= p
                    
    indices = [] # index of discovery
    xlist = [] #original x terms
    smooth_nums = []
    
    # теперь sieve_list будет содержать только единицы и те числа, простые делители которых
    # больше заданного B (то есть эти числа не будут B-гладкими)
    # значит, их мы убираем, а вот числа, которые превратились в 1, добавляем в smooth_nums
    for i in range(len(sieve_list)):
        if len(smooth_nums) >= len(factor_base)+1:
            break
        elif sieve_list[i] == 1 or sieve_list[i] == -1: # found B-smooth number
            smooth_nums.append(sieve_seq[i])
            xlist.append(i+root-I)
            indices.append(i)
    return smooth_nums, xlist, indices

# метод Гаусса
def gauss_elim(M):
    marks = [False]*len(M[0])
    
    for i in range(len(M)):
        for j in range(len(M[i])):
            num = M[i][j]
            row = M[i]
            if num == 1:
                marks[j] = True
                for k in chain(range(0,i),range(i+1,len(M))): #search for other 1s in the same column
                    if M[k][j] == 1:
                        for i in range(len(M[k])):
                            M[k][i] = (M[k][i] + row[i])%2
                break
    M = transpose(M)
    
    sol_rows = []
    for i in range(len(marks)): #find free columns (which have now become rows)
        if not marks[i]:
            free_row = [M[i],i]
            sol_rows.append(free_row)
    
    if not sol_rows:
        return "No solution found. Need more smooth numbers."

    return sol_rows, marks, M

# пытаемся превратить выбранную строку матрицы M в строку из нулей
# через линейные преобразования
def solve_row(sol_rows, M, marks, K=0):
    solution_vec, indices = [],[]
    free_row = sol_rows[K][0] # may be multiple K
    for i in range(len(free_row)):
        if free_row[i] == 1:
            indices.append(i)
    
    for r in range(len(M)): #rows with 1 in the same column will be dependent
        if not marks[r]:
            continue

        for i in indices:
            if M[r][i] == 1:
                solution_vec.append(r)
                break

    solution_vec.append(sol_rows[K][1])       
    return solution_vec

# тут считаем произведение x_i, которые мы предварительно выбрали
# и произведение чисел (x_i*x_i - N)
# получается, что последнее прозведение имеет (с какой-то вероятностью)
# нетривиальный общий делитель
# значит, можем через алгоритм Евклида найти НОД - это будет один из делителей
def solve(solution_vec, smooth_nums, xlist, N):
    
    solution_nums = [smooth_nums[i] for i in solution_vec]
    x_nums = [xlist[i] for i in solution_vec]
    print(solution_nums,x_nums)
    
    Asquare = 1
    for n in solution_nums:
        Asquare *= n
        
    b = 1
    for n in x_nums:
        b *= n

    a = isqrt(Asquare)    
    factor, x1, y1 = euclid(b-a,N)
    return factor

# функция, раскладывающая N на p и q
# n - число N
# B - максимальный простой делитель у x_i, которые мы будем перебирать
# I - будем перебирать x_i в интервале [sqrt(N) - I; sqrt(N) + I]
def find_factors(N, B, I):
    # если простое, то разложить не получится
    if is_prime(N):
        return (None, None)
    
    # пытаемся найти такое число х, что х*х == N
    real_sqrt = isqrt(N)
    if real_sqrt is not None:
        # если такое число нашлось, то число N = x*x
        return (real_sqrt, real_sqrt)
    
    # находим факторную базу
    factor_base = find_base(N,B) # простые числа
    
    # вычисляем B-гладкие числа
    smooth_nums, xlist, indices = find_smooth1(factor_base, N,I)
    
    if len(smooth_nums) < len(factor_base):
        return ("Мало B-гладких чисел, необходимо увеличить параметр B.", None)
    
    # строим матрицу из 1 и 0
    is_square, t_matrix = build_matrix(smooth_nums,factor_base)

    # если сразу нашли нулевую строку, то нашли и делители
    if is_square == True:
        x = smooth_nums.index(t_matrix)
        factor, x1, y1 = euclid(xlist[x]+int(sqrt(t_matrix)),N)
        return abs(int(factor)), abs(int(N//factor))

    # иначе приводим эту матрицу к ступенчатому виду через метод Гаусса
    sol_rows,marks,M = gauss_elim(t_matrix)

    # затем берем первый вектор и пытаемся его привести к нулевому
    solution_vec = solve_row(sol_rows,M,marks,0)

    # вычисляем делитель числа N
    factor = solve(solution_vec,smooth_nums,xlist,N)

    for K in range(1,len(sol_rows)):
        # если на K-ой попытке снова нашли тривиальный делитель
        # то продолжаем искать
        if factor == 1 or factor == N:
            solution_vec = solve_row(sol_rows,M,marks,K)
            factor = solve(solution_vec,smooth_nums,xlist,N)
        else:
            # иначе выводим ответ
            return abs(int(factor)), abs(int(N//factor))

    # не получили ответ, плачем 0_0
    return (None, None)

@app.route('/vzlom',methods=["POST"])
def vzlom():
    res = json.loads(request.get_data())
    N = int(res['N'])
    e = int(res['e'])
    text = res['text']


    B = 15000
    I = 15000
    p, q = find_factors(N, B, I)
    if(q is None): return json.dumps({'status': 'ok', 'errorN': 'yes', 'p': p})
    fiN = (p - 1)*(q - 1)
    d, x, y = euclid(e, fiN)
    if d != 1:
        raise ValueError()
    else:
        x = (x % fiN + fiN) % fiN

    print('Вычисленное p: ' + str(p))
    print('Вычисленное q: ' + str(q))
    print('Вычисленное d: ' + str(x))

    message = decrypt(text, x, N)
    if(message == 'error'):
        return json.dumps({'status': 'ok', 'error': 'error'})
    return json.dumps({'status': 'ok', 'result': {"d": str(x), 'mes': message}})
    

if __name__ == '__main__':
    app.run(debug=True, host="localhost", port='5000')