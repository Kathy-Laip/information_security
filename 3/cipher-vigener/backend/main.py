from flask import Flask, request
import json
from collections import Counter

# app = Flask(__name__)
app = Flask(__name__.split('.')[0])

alphaENG = [
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
]

alphaRUS = [
    'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ1234567890'
]

popularRU = 'О'
popularEN = 'E'

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

def calculate_index(text, language):
    total_count = 0
    char_count = [0] * 43

    for s in text: 
        if(language == 'EN'):
            char_count[alphaENG[0].find(s)] += 1
        elif(language == 'RU'):
            print(s)
            char_count[alphaRUS[0].find(s)] += 1
        total_count += 1
    
    index_of_coincidence = 0.0
    if total_count > 1:
        for count in char_count:
            index_of_coincidence += (count * (count - 1)) / (total_count * (total_count - 1))

    return index_of_coincidence

def decipher(key, setting, text):
    ost = len(text)%len(key)
    newKey = key*(int(len(text)/len(key))) + key[:ost]
    
    deCipherText = ''
    if setting == 'RU':
        for i in range(len(text)):
            pos = (alphaRUS[0].find(text[i]) - alphaRUS[0].find(newKey[i])) % len(alphaRUS[0])
            deCipherText += alphaRUS[0][pos]
    elif setting == 'EN':
        for i in range(len(text)):
            pos = (alphaENG[0].find(text[i]) - alphaENG[0].find(newKey[i])) % len(alphaENG[0])
            deCipherText += alphaENG[0][pos]

    return deCipherText

@app.route('/vzlom', methods=['POST'])
def vzlom():
    data = json.loads(request.get_data())
    text = data["text"]
    language = data['set']

    potential_key_lengths = 0 # предлполагаемая длина ключа
    for length in range(1, len(text)):
        subtexts = [text[i::length] for i in range(length)]
        indices_of_coincidence = [calculate_index(stext, language) for stext in subtexts]
        average_index_of_coincidence = sum(indices_of_coincidence) / length

        if language == "EN":
            expected_index = 0.067
        else:
            expected_index = 0.053

        if abs(average_index_of_coincidence - expected_index) < 0.01:
            potential_key_lengths = length; break

    key = ''

    for i in range(potential_key_lengths):
        substring = text[i::potential_key_lengths]
        freq_analysis = Counter(substring)
        sorted_freq = sorted(freq_analysis.items(), key=lambda x: x[1], reverse=True)
        print(sorted_freq)
        most_common_char = sorted_freq[0][0]
        if(language == 'RU'):
            pos = (alphaRUS[0].find(most_common_char) - alphaRUS[0].find(popularRU)) % len(alphaRUS[0])
            key += alphaRUS[0][pos]
        if(language == 'EN'):
            pos = (alphaENG[0].find(most_common_char) - alphaENG[0].find(popularEN)) % len(alphaENG[0])
            key += alphaENG[0][pos]

    decText = decipher(key, language, text)

    return json.dumps({'status': 'ok', 'key': key, 'text': decText})        

if __name__ == '__main__':
    app.run(debug=True, host="localhost", port='5000')
    
