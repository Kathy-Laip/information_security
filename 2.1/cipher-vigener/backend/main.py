from flask import Flask, request
import json

# app = Flask(__name__)
app = Flask(__name__.split('.')[0])

alphaENG = [
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
]

alphaRUS = [
    'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ1234567890'
]

def checkKeyText(key, text):
    return True if len(text) >= len(key) else False

def checkText(setting, text):
    if setting == 'RU':
        for i in range(len(text)):
            if(text[i] not in alphaRUS[0]): return False
    elif setting == 'EN':
        for i in range(len(text)):
            if(text[i] not in alphaENG[0]): return False
    return True


@app.route('/cipher', methods=["POST"])
def cipher():
    res = json.loads(request.get_data())
    key = res["key"]
    setting = res["set"]
    text = res["text"]

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

    if(checkText(setting, newText) == False): return json.dumps({"status": "inCorrectText"})
    if(newText == ''): return json.dumps({'status': 'isEmpty'})
    if(checkKeyText(key, newText) == False): return json.dumps({"status": "inCorrectTextWithKey"})

    ost = len(text)%len(key)
    newKey = key*(int(len(text)/len(key))) + key[:ost]
    # print(newKey)
    # print(newText)

    cipherText = ''
    if setting == 'RU':
        for i in range(len(newText)):
            pos = (alphaRUS[0].find(newText[i]) + alphaRUS[0].find(newKey[i])) % len(alphaRUS[0])
            cipherText += alphaRUS[0][pos]
    elif setting == 'EN':
        for i in range(len(newText)):
            pos = (alphaENG[0].find(newText[i]) + alphaENG[0].find(newKey[i])) % len(alphaENG[0])
            cipherText += alphaENG[0][pos]
    
    
    return json.dumps({"status": 'ok', "text": cipherText})

@app.route('/decipher', methods=["POST"])
def decipher():
    res = json.loads(request.get_data())
    key = res["key"]
    setting = res['set']
    text = res["text"]

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

    if(checkText(setting, newText) == False): return json.dumps({"status": "inCorrectText"})
    if(newText == ''): return json.dumps({'status': 'isEmpty'})
    if(checkKeyText(key, newText) == False): return json.dumps({"status": "inCorrectTextWithKey"})


    ost = len(text)%len(key)
    newKey = key*(int(len(text)/len(key))) + key[:ost]
    
    deCipherText = ''
    if setting == 'RU':
        for i in range(len(newText)):
            pos = (alphaRUS[0].find(newText[i]) - alphaRUS[0].find(newKey[i])) % len(alphaRUS[0])
            deCipherText += alphaRUS[0][pos]
    elif setting == 'EN':
        for i in range(len(newText)):
            pos = (alphaENG[0].find(newText[i]) - alphaENG[0].find(newKey[i])) % len(alphaENG[0])
            deCipherText += alphaENG[0][pos]

    return json.dumps({"status": 'ok', "text": deCipherText})
        

if __name__ == '__main__':
    app.run(debug=True, host="localhost", port='5000')