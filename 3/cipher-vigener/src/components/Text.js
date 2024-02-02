import React from "react";


async function apiData(obj, strAPI) {
    try{
        let res = await fetch(strAPI,{
            method: 'POST',
            body: JSON.stringify(obj),
            headers:{
                'Content-Type': 'application/json'
            }
        })
        let result = await res.json()
        return result
    }
    catch{
        alert('Что-то не так с данными')
    }
}


class Text extends React.Component{
    constructor(options){
        super(options)
    }

    cipherFromFile = () => {
        let reader = new FileReader()
        let key = document.getElementById('key')
        let select = document.getElementById('set')
        let textCipher = document.getElementById('textCrypt')
        let keyValue = document.getElementById('key').value
        let file = document.getElementById("file").files[0]
        let selectValue = document.getElementById('set').value

        if(!keyValue || !file || !selectValue){
            alert('заполните все поля!!!')
            key.style.border = '10px solid red'
            select.style.border = '10px solid red'
        } else{
            key.style.border = '1px solid black'
            select.style.border = '1px solid black'
            reader.readAsText(file, 'utf-8')
            reader.onload = () => {
                let obj = {
                    'key': keyValue,
                    'text': reader.result,
                    'set': selectValue
                }
                let res = apiData(obj, '/cipher')
                res.then(value => {
                    if(value.status === 'inCorrectKey'){
                        alert('Что-то не так с ключом')
                    }
                    if(value.status === 'inCorrectText'){
                        alert('Что-то не так с текстом')
                    }
                    if(value.status === "inCorrectTextWithKey"){
                        alert('Ключ больше, чем текст')
                    }
                    if(value.status === 'isEmpty'){
                        alert('Возможно шифровать нечего, шифрование невозможно')
                    }
                    if(value.status === 'ok'){
                        textCipher.innerHTML = value.text
                    }
                })
            }
        }
    }

    vzlom(){
        let textCipher = document.getElementById('textCrypt').value
        let setting = document.getElementById('set').value
        let keyVzlom = document.getElementById('keyVzlom')
        let textVzlom = document.getElementById('textVzlom')

        if(!textCipher && !setting) alert('Заполни поле зашифрованного текста и настройки языка')

        let res = apiData({"text": textCipher, "set": setting}, '/vzlom')
        res.then(value => {
            if(value.status === 'ok') keyVzlom.innerHTML = value.key; textVzlom.innerHTML = value.text
        })

    }

    render(){
        return(
            <main> 
                <div className="text">
                    <p>Введите ключ</p>
                    <textarea id="key"></textarea>
                </div>
                <div className="settings">
                    <p>Выберите язык</p>
                    <select id='set'>
                        <option value="RU">RU</option>
                        <option value="EN">EN</option>
                    </select>
                </div>
                <div className="text">
                    <p>Зашифрованный текст</p>
                    <textarea id="textCrypt" disabled></textarea>
                </div>
                <button className="btn" onClick={this.vzlom}>
                    Взлом
                </button>
                <div className="text">
                    <p>Загрузите файл:</p>
                    <input type="file" id="file"></input>
                </div>
                <button className="btn" onClick={this.cipherFromFile}>
                    Зашифровать из файла
                </button>
                <div className="text">
                    <p>Взломанный ключ</p>
                    <textarea id="keyVzlom"></textarea>
                </div>
                <div className="text">
                    <p>Взоманный текст</p>
                    <textarea id="textVzlom"></textarea>
                </div>
            </main>
        )
    }
}

export default Text