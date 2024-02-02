from flask import Flask, request
import json
from application import Application

# app = Flask(__name__)
app = Flask(__name__.split('.')[0])

alphaENG = [
    'abcdefghijklmnopqrstuvwxyz',
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
]

alphaRUS = [
    'абвгдеёжзийклмнопрстуфхцчшщъыьэюя',
    'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
]

number = '0123456789'

@app.route('/test',methods=["POST"])
def test():
    res = json.loads(request.get_data())
    key = res["key"]
    text = res["text"].split()
    setting = res["set"]

    # print(key, text, setting)
    if key[0] == '-':
        for i in range(1, len(key)):
            if(key[i] not in number): return json.dumps({"status": 'inCorrectKey'})
    else:
        for i in range(len(key)):
            if(key[i] not in number): return json.dumps({"status": 'inCorrectKey'})

    key = int(key)

    correct = False
    if setting == 'RU':
        for i in range(len(text)):
            correct = all([x.lower() in alphaRUS[0] for x in text[i]])
            if(not correct): return json.dumps({"status": 'inCorrect'})
    elif setting == 'EN':
        for i in range(len(text)):
            correct = all([x.lower() in alphaENG[0] for x in text[i]])
            if(not correct): return json.dumps({"status": 'inCorrect'})


    textCipher = []
    if setting == 'RU':
        for i in range(len(text)):
            row = ''
            for j in range(len(text[i])):
                if(text[i][j] in alphaRUS[0]):
                    mesto = alphaRUS[0].find(text[i][j])
                    new_mesto = (mesto + key) % len(alphaRUS[0])
                    # print(new_mesto)
                    row += alphaRUS[0][new_mesto]
                elif(text[i][j] in alphaRUS[1]):
                    mesto = alphaRUS[1].find(text[i][j])
                    new_mesto = (mesto + key) % len(alphaRUS[0])
                    # print(new_mesto)
                    row += alphaRUS[1][new_mesto]
            textCipher.append(row)
    elif setting == 'EN':
        for i in range(len(text)):
            row = ''
            for j in range(len(text[i])):
                if(text[i][j] in alphaENG[0]):
                    mesto = alphaENG[0].find(text[i][j])
                    new_mesto = (mesto + key) % len(alphaENG[0])
                    # print(new_mesto)
                    row += alphaENG[0][new_mesto]
                elif(text[i][j] in alphaENG[1]):
                    mesto = alphaENG[1].find(text[i][j])
                    new_mesto = (mesto + key) % len(alphaENG[0])
                    # print(new_mesto)
                    row += alphaENG[1][new_mesto]
            textCipher.append(row)
    textCipher = ' '.join(textCipher)
    # print(textCipher)
    return json.dumps({"status": 'ok', "textCipher": textCipher})

@app.route("/decipher",methods=["POST"])
def decipher():
    res = json.loads(request.get_data())
    key = res["key"]
    text = res["text"].split()
    setting = res["set"]


    if key[0] == '-':
        for i in range(1, len(key)):
            if(key[i] not in number): return json.dumps({"status": 'inCorrectKey'})
    else:
        for i in range(len(key)):
            if(key[i] not in number): return json.dumps({"status": 'inCorrectKey'})

    key = int(key) * (-1)

    correct = False
    if setting == 'RU':
        for i in range(len(text)):
            correct = all([x.lower() in alphaRUS[0] for x in text[i]])
            if(correct == False): return json.dumps({"status": 'inCorrect'})
    elif setting == 'EN':
        for i in range(len(text)):
            correct = all([x.lower() in alphaENG[0] for x in text[i]])
            if(correct == False): return json.dumps({"status": 'inCorrect'})


    textCipher = []
    if setting == 'RU':
        for i in range(len(text)):
            row = ''
            for j in range(len(text[i])):
                if(text[i][j] in alphaRUS[0]):
                    mesto = alphaRUS[0].find(text[i][j])
                    new_mesto = (mesto + key) % len(alphaRUS[0])
                    # print(new_mesto)
                    row += alphaRUS[0][new_mesto]
                elif(text[i][j] in alphaRUS[1]):
                    mesto = alphaRUS[1].find(text[i][j])
                    new_mesto = (mesto + key) % len(alphaRUS[0])
                    # print(new_mesto)
                    row += alphaRUS[1][new_mesto]
            textCipher.append(row)
    elif setting == 'EN':
        for i in range(len(text)):
            row = ''
            for j in range(len(text[i])):
                if(text[i][j] in alphaENG[0]):
                    mesto = alphaENG[0].find(text[i][j])
                    new_mesto = (mesto + key) % len(alphaENG[0])
                    # print(new_mesto)
                    row += alphaENG[0][new_mesto]
                elif(text[i][j] in alphaENG[1]):
                    mesto = alphaENG[1].find(text[i][j])
                    new_mesto = (mesto + key) % len(alphaENG[0])
                    # print(new_mesto)
                    row += alphaENG[1][new_mesto]
            textCipher.append(row)
    textCipher = ' '.join(textCipher)
    # print(textCipher)
    return json.dumps({"status": 'ok', "textDeCipher": textCipher})

if __name__ == '__main__':
    app.run(debug=True, host="localhost", port='5000')