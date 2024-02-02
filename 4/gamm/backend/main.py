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

    if(len(newBitText) == len(key)):
        flag = True
    elif(len(newBitKey) == len(newBitText)):
        flag = False
    elif(len(newBitText) > len(newBitKey)):
        count = len(newBitText)//len(newBitKey)
        ost = len(newBitText)%len(newBitKey)
        newBitKey = newBitKey * count + newBitKey[0:ost]
        flag = False
        print((newBitKey))
    elif(len(newBitText) < len(newBitKey)):
        newBitKey = newBitKey[:len(newBitText)]
        flag = False
    else:
        return json.dumps({'status': 'lenTextKey'})

    if(flag):
        textCrypt = xor(newBitText, key)
    else: textCrypt = xor(newBitText, newBitKey)

    with open('text.txt','w') as f1:
        pass
    with open('text.txt', 'a', encoding='utf-8') as f1:
        f1.writelines(textCrypt)
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

    flag = True
    if(len(text[0]) == len(key)):
        flag = True
    elif(len(newBitKey) == len(text[0])):
        flag = False
    elif(len(text[0]) > len(newBitKey)):
        count = len(text[0])//len(newBitKey)
        ost = len(text[0])%len(newBitKey)
        newBitKey = newBitKey * count + newBitKey[0:ost]
        flag = False
        print((newBitKey))
    elif(len(text[0]) < len(newBitKey)):
        newBitKey = newBitKey[:len(text[0])]
        flag = False
    else:
        return json.dumps({'status': 'lenTextKey'})

    if(flag):
        res = xor(text[0], key)
    else: res = xor(text[0], newBitKey)

    newText = bytes.decode(convert_to_byte(res), encoding='utf-8')
    return json.dumps({'status': 'ok', 'text': newText})

@app.route('/gener', methods=["POST"])
def gener():
    res = json.loads(request.get_data())
    text = res["text"]
    setting = res["set"]

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

    binary_s_len = len(convert_to_bitstring(bytes(newText, 'utf-8')))
    zeros_positions = random.sample(range(0, binary_s_len), binary_s_len // 2)


    key = ''
    for i in range(binary_s_len):
        # если текущий индекс есть среди позиций нулей, то кладем туда ноль
        if i in zeros_positions:
            key += '0'
        else:
            key += '1' # иначе единицу


    return json.dumps({"status": 'ok', "text": key})

if __name__ == '__main__':
    app.run(debug=True, host="localhost", port='5000')