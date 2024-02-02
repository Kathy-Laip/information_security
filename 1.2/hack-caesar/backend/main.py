from flask import Flask, request
import json
from application import Application

app = Flask(__name__)
# app = Flask(__name__.split('.')[0])

alphaENG = [
    'abcdefghijklmnopqrstuvwxyz',
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
]

alphaRUS = [
    'абвгдеёжзийклмнопрстуфхцчшщъыьэюя',
    'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
]

number = '0123456789'

popularRU = 'о'
popularEN = 'e'

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


    with open('text.txt','w') as f1:
        pass
    with open('text.txt', 'a', encoding='utf-8') as f1:
        f1.writelines(textCipher)
    return json.dumps({"status": 'ok'})

@app.route('/hack',methods=["GET"])
def hack():
    set = ''
    with open('text.txt', 'r', encoding="utf-8") as f1:
        text = f1.readlines()

    if text[0][0].lower() in alphaENG[0]: 
        set = 'EN'
    elif text[0][0].lower() in alphaRUS[0]: 
        set = 'RU' 

    dictonary = dict()
    
    for row in text:
        row = row.split()
        for word in row:
            for letter in word:
                dictonary[letter.lower()] = dictonary.get(letter.lower(), 0) + 1

    maximum = max(dictonary.items(), key=lambda item: item[1])[0]
    if set == 'RU':
        key = (alphaRUS[0].find(maximum) - alphaRUS[0].find(popularRU)) 
    else:
        key = (alphaENG[0].find(maximum) - alphaENG[0].find(popularEN)) 
            
    print(set)
    print(key)
    print(maximum)
    print(dictonary)
    textAgain = []
    if set == 'RU':
        for row in text:
            row = row.split()
            seq = []
            for word in row:
                seqWord = ''
                for letter in word:
                    if(letter in alphaRUS[0]):
                        mesto = alphaRUS[0].find(letter)
                        new_mesto = (mesto - key) % len(alphaRUS[0])
                        seqWord += alphaRUS[0][new_mesto]
                    elif(letter in alphaRUS[1]):
                        mesto = alphaRUS[1].find(letter)
                        new_mesto = (mesto - key) % len(alphaRUS[1])
                        seqWord += alphaRUS[1][new_mesto]
                seq.append(seqWord)
            rowAgain = ' '.join(seq)
        textAgain.append(rowAgain)
    elif set == 'EN':
        for row in text:
            print(row)
            row = row.split()
            seq = []
            for word in row:
                seqWord = ''
                for letter in word:
                    if(letter in alphaENG[0]):
                        mesto = alphaENG[0].find(letter)
                        new_mesto = (mesto - key) % len(alphaENG[0])
                        seqWord += alphaENG[0][new_mesto]
                    elif(letter in alphaENG[1]):
                        mesto = alphaENG[1].find(letter)
                        new_mesto = (mesto - key) % len(alphaENG[1])
                        seqWord += alphaENG[1][new_mesto]
                seq.append(seqWord)
            rowAgain = ' '.join(seq)
        textAgain.append(rowAgain)

    print(textAgain)

    return json.dumps({'status':'ok', "text": textAgain})

if __name__ == '__main__':
    app.run(debug=True, host="localhost", port='5000')