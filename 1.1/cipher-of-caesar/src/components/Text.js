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
        this.cipher = this.cipher.bind(this)
    }


    cipher = () => {
        let key = document.getElementById('key')
        let text = document.getElementById('text')
        let select = document.getElementById('set')
        let textCipher = document.getElementById('textCrypt')
        let keyValue = document.getElementById('key').value
        let textValue = document.getElementById('text').value
        let selectValue = document.getElementById('set').value

        if(!keyValue || !textValue || !selectValue){
            alert('заполните все поля!!!')
            key.style.border = '10px solid red'
            text.style.border = '10px solid red'
            select.style.border = '10px solid red'
        } else{
            key.style.border = '1px solid black'
            text.style.border = '1px solid black'
            select.style.border = '1px solid black'
            let obj = {
                'key': keyValue,
                'text': textValue,
                'set': selectValue
            }
            console.log(obj)
            let res = apiData(obj, '/test')
            console.log(res)
            res.then(value => {
                if(value.status === 'inCorrectKey'){
                    alert('Что-то не так с ключом')
                }
                if(value.status === 'inCorrect'){
                    alert('Что-то не так с текстом')
                }
                if(value.status === 'ok'){
                    textCipher.innerHTML = value.textCipher
                }
            })
            
        }
    }

    decipher = () => {
        let key = document.getElementById('key')
        let text = document.getElementById('text')
        let select = document.getElementById('set')
        let textDeCipher = document.getElementById('textNormal')
        let keyValue = document.getElementById('key').value
        let textValue = document.getElementById('text').value
        let selectValue = document.getElementById('set').value

        if(!keyValue || !textValue || !selectValue){
            alert('заполните все поля!!!')
            key.style.border = '10px solid red'
            text.style.border = '10px solid red'
            select.style.border = '10px solid red'
        } else{
            key.style.border = '1px solid black'
            text.style.border = '1px solid black'
            select.style.border = '1px solid black'
            let obj = {
                'key': keyValue,
                'text': textValue,
                'set': selectValue
            }
            let res = apiData(obj, '/decipher')
            res.then(value => {
                if(value.status === 'inCorrectKey'){
                    alert('Что-то не так с ключом')
                }
                if(value.status === 'inCorrect'){
                    alert('Что-то не так с текстом')
                }
                if(value.status === 'ok'){
                    textDeCipher.innerHTML = value.textDeCipher
                }
            })
            
        }
    }

    render(){
        return (
            <main>
                <div className="text">
                    <p>Введите текст</p>
                    <textarea id="text"></textarea>
                </div>
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
                <button className="btn" onClick={this.cipher}>
                    Зашифровать
                </button>
                <div className="text">
                    <p>Зашифрованный текст</p>
                    <textarea id="textCrypt"></textarea>
                </div>
                <button className="btn" onClick={this.decipher}>
                    Расшифровать
                </button>
                <div className="text">
                    <p>Расшифрованный текста</p>
                    <textarea id="textNormal"></textarea>
                </div>
            </main>

        )
    }
}

export default Text