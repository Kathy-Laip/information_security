import random

def get_key(key, text_len): # генерирует последовательность чисел, которая будет перестановкой rc4
    S = list(range(256)) # инициализируем массив из [0,...,255] чисел
    j = 0
    res = [] # результирующая последовательность

    # вычисление последовательности (KSA)
    for i in range(256):
        j = (j + S[i] + key) % 256 # считаем индекс элемента, который будем менять местами с i-ым элементом
        S[i], S[j] = S[j], S[i]

    # псевдо-рандомный алгоритм шифрования (PRGA)
    i = j = 0
    for _ in range(text_len): # генерируем последовательность, которая будет перестановкой
        i = (i + 1) % 256 # вычисляем индексы элементов массива S, которые будем менять местами
        j = (j + S[i]) % 256
        
        S[i], S[j] = S[j], S[i]
        k = S[(S[i] + S[j]) % 256] # вычисляем элемент последовательности для rc4
        res.append(k)
    
    return res

def rc4(key, text):
    k = get_key(key, len(text))
    res = []

    for i, char in zip(range(len(text)), text): 
        # проходимся по сообщению и каждый элемент строки text шифруем через последовательность rc4
        res.append(chr(ord(char) ^ k[i]))

    return ''.join(res)

def generate_key_sequence(key_len):
    return random.sample(list(range(0, 256))*5, key_len)

if __name__ == '__main__':
    key = generate_key_sequence(1)
    plaintext = "Hello, World!"
    ciphertext = rc4(key, plaintext)
    print("Ciphertext:", ciphertext)
    deciphertext = rc4(key, ciphertext)
    print(deciphertext)