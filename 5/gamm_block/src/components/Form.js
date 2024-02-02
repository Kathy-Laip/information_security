import React, { Component } from 'react'

async function apiPos(obj, url){
    try{
        let res = await fetch(url, {
            method: 'POST',
            body: JSON.stringify(obj)
        })
        let result = await res.json()
        return result
    }
    catch{
        alert('Соединение с сервером не установлено, [POST]')
    }
}

export class Form extends Component {
    constructor(options){
        super(options)
    }

    render() {
      return (
      <main>
          <div className="text">
              <p>Исходный текст</p>
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
          <div className='text'>
              <p>Результат после расшифрования</p>
              <textarea rows={10} id="textCrypt"></textarea>
          </div>
          <button className="btn" onClick={this.decipher}>
              Расшифровать
          </button>
      </main>
      )
    }

    decipher(){
        let key = document.getElementById('key')
        let set = document.getElementById('set').value
        let keyValue = document.getElementById('key').value
        let textCyprt = document.getElementById('textCrypt')

        if(!keyValue || !set ){
            alert('Заполните все поля!!!')
            key.style.border = '10px solid red'
        } else{
            key.style.border = '1px solid black'

            let obj = {
                'key': keyValue,
                'set': set
            }

            let res = apiPos(obj, '/decipher')
            res.then(value => {
                if(value.status === 'inCorrectKey'){
                    alert('Что-то не так с ключом')
                }
                if(value.status === 'lenTextKey'){
                    alert('Длины текста и ключа не совпадают')
                }
                if(value.status === 'ok'){
                    textCyprt.innerHTML = value.text
                }
            })
        }
    }


    cipher(){
        let text = document.getElementById('text')
        let key = document.getElementById('key')
        let set = document.getElementById('set').value
        let textValue = document.getElementById('text').value
        let keyValue = document.getElementById('key').value

        if(!keyValue || !set || !textValue){
            alert('Заполните все поля!!!')
            key.style.border = '10px solid red'
            text.style.border = '10px solid red'
        } else{
            key.style.border = '1px solid black'
            text.style.border = '1px solid black'

            let obj = {
                'key': keyValue,
                'text': textValue,
                'set': set
            }

            let res = apiPos(obj, '/cipher')
            res.then(value => {
                if(value.status === 'inCorrectKey'){
                    alert('Что-то не так с ключом')
                }
                if(value.status === 'isEmpty'){
                    alert('Шифровать нечего')
                }
                if(value.status === 'lenTextKey'){
                    alert('Длины ключа больше текста')
                }
                if(value.status === 'ok'){
                    alert('Данные успешно записаны')
                }
            })
        }

    }
}

export default Form