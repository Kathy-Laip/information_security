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

async function apiGet(strAPI){
    try{
        let res = await fetch(strAPI)
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

    cipher = () => {
        let reader = new FileReader()
        let key = document.getElementById('key')
        let select = document.getElementById('set')
        let file = document.getElementById("file").files[0]
        let keyValue = document.getElementById('key').value
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
                // console.log(obj)
                let res = apiData(obj, '/test')
                res.then(value => {
                    if(value.status === 'inCorrectKey'){
                        alert('Что-то не так с ключом')
                    }
                    if(value.status === 'inCorrect'){
                        alert('Что-то не так с текстом')
                    }
                    if(value.status === 'ok'){
                        alert('Данные успешно записаны')
                    }
                })
            }
            
        }
    }

    hack = () => {
        let textNormal = document.getElementById('textNormal')
        let res = apiGet('/hack')
        res.then(value => {
            if(value.status === 'ok'){
                textNormal.innerHTML = value.text
            }
        })
    }

    render(){
        return(
            <main>
                <div className="inputText">
                    <p>Загрузите файл:</p>
                    <input type="file" id="file"></input>
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
                <div className="textHack">
                    <p>Взломанный текст</p>
                    <textarea id="textNormal"></textarea>
                </div>
                <button className="btn" onClick={this.hack}>
                    Взлом
                </button>
            </main>
        )
    }
}

export default Text