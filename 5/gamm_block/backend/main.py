from flask import Flask, request
import json
from application import Application
from functools import reduce
import random

app = Flask(__name__)

alphaENG = [
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
]

alphaRUS = [
    'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ0123456789'
]


def checkText(setting, text):
    if setting == 'RU':
        for i in range(len(text)):
            if(text[i] not in alphaRUS[0]): return False
    elif setting == 'EN':
        for i in range(len(text)):
            if(text[i] not in alphaENG[0]): return False
    return True

# конвертирует с биты
def convert_to_bitstring(s):
    result = []
    numbers = [*map(lambda a: int(a), s)] # каждый символ преобразовываем в int

    for number in numbers: # перебираем каждый int символ
        number_res = [] # массив для записи каждого символы, добавляем сюда 1 и 0
        for i in range(8): # 8 так как в массиве 8 бит..
            number_res.append(f'{1 if number % 2 != 0 else 0}') # делим наш символ на 2 и смотрим остаток
            number //= 2 # делим наш символ, переход к новому биту
        number_res.reverse() # переворачиваем наши биты
        result.append(number_res) # вставляем в результат 
    return ''.join(reduce(lambda a, b: a + b, result)) # соединяем все битики в целое

def convert_to_byte(s):
    byte_size = 8 # в строке выделяем блок по 8, то есть выделяем целый вит
    result = []
    for byte in [s[i:i+byte_size] for i in range(0, len(s), byte_size)]: # проходмся по всей строке и выделяем блоки по 8 
        number = 0 # наш байт нормальный
        dvoika = 128 # сколько будем прибавлять
        for bit in byte: # проходимся по битикам
            if bit == '1': # если единичку встретили, то прибавляем степень двойки
                number += dvoika
            dvoika //= 2
        result.append(number) # преобразовываем в символ и добавляем в массив

    return bytes(result) # соединяем все наши символы в массив байтов

def xor(first: str, second: str) -> str:    
    res = ''
    for i in range(len(first)):
        if first[i] == second[i]:
            res += '0'
        else:
            res += '1'

    return res

@app.route('/cipher',methods=["POST"])
def test():
    res = json.loads(request.get_data())
    key = res["key"]
    text = res["text"]
    setting = res["set"]
    
    if(checkText(setting, key) == False): return json.dumps({"status": 'inCorrectKey'})

    newText =  ''
    if setting == 'RU':
        for letter in text:
            if(letter in alphaRUS[0]):
                newText += letter
    elif setting == 'EN':
        for letter in text:
            if(letter in alphaENG[0]):
                newText += letter

    if(newText == ''): return json.dumps({'status': 'isEmpty'})

    newBitText = convert_to_bitstring(bytes(newText, encoding='utf-8'))
    newBitKey = convert_to_bitstring(bytes(key, encoding='utf-8'))
    flag = True

    if(len(newBitKey) > len(newBitText)): return json.dumps({'status': 'lenTextKey'})

    newBitShif = ''
    for i in range(0, len(newBitText), len(newBitKey)):
        lenn = min(len(newBitText) - i, len(newBitKey))
        newS = xor(newBitText[i : i + lenn], newBitKey[0 : lenn])
        newBitKey = newS
        newBitShif += newS

    with open('text.txt','w') as f1:
        pass
    with open('text.txt', 'a', encoding='utf-8') as f1:
        f1.writelines(newBitShif)
    return json.dumps({'status': 'ok'})

@app.route('/decipher',methods=["POST"])
def decipher():
    res = json.loads(request.get_data())
    key = res["key"]
    setting = res["set"]

    if(checkText(setting, key) == False): return json.dumps({"status": 'inCorrectKey'})

    with open('text.txt', 'r', encoding="utf-8") as f1:
        text = f1.readlines()

    newBitKey = convert_to_bitstring(bytes(key, encoding='utf-8'))

    newRachif = ''
    print(newBitKey)
    print(text)

    for i in range(0, len(text[0]), len(newBitKey)):
        lenn = min(len(text[0]) - i, len(newBitKey))
        newBlock = xor(text[0][i : i + lenn], newBitKey[0 : lenn])
        newRachif += newBlock
        newBitKey = text[0][i:i + len(newBitKey)]

    print(newRachif)
    res = bytes.decode(convert_to_byte(newRachif), encoding='utf-8')
    return json.dumps({'status': 'ok', 'text': res})

if __name__ == '__main__':
    app.run(debug=True, host="localhost", port='5000')