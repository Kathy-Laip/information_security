import React, { Component } from 'react'
/* global BigInt */

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
              <p>Биты</p>
              <textarea id="bits">512</textarea>
          </div>
          <button className="btn" onClick={this.gener}>
              Сгенерировать ключи
          </button>
          <div className="text">
              <p>p = </p>
              <textarea disabled id="p"></textarea>
          </div>
          <button className="btn" onClick={this.cipher}>
              Зашифровать
          </button>
          <div className="text">
              <p>q = </p>
              <textarea disabled id="q"></textarea>
          </div>
          <button className="btn" onClick={this.decipher}>
              Расшифровать
          </button>
          <div className="text">
              <p>e = </p>
              <textarea disabled id="e"></textarea>
          </div>
          <div className="text">
              <p>d = </p>
              <textarea disabled id="d"></textarea>
          </div>
          <div className="text">
              <p>φ(N) = </p>
              <textarea disabled id="fi(N)"></textarea>
          </div>
          <div className="text">
              <p>N = </p>
              <textarea disabled id="N"></textarea>
          </div>
          <div className="text">
              <p>Исходный текст </p>
              <textarea rows={5} id="text"></textarea>
          </div>

          <div className='text'>
              <p>Криптограмма</p>
              <textarea rows={5} id="textCrypt"></textarea>
          </div>
      </main>
      )
    }

    gener(){
        let bits = document.getElementById('bits').value

        let p = document.getElementById('p')
        let q = document.getElementById('q')
        let e = document.getElementById('e')
        let d = document.getElementById('d')
        let fiN = document.getElementById('fi(N)')
        let N = document.getElementById('N')

        if(/\d+/.test(bits) && bits !== '0'){
            let res = apiPos({'bits': bits}, '/gener')
            res.then(res => {
                if(res.status === 'ok'){
                    p.innerHTML = res.result.p
                    q.innerHTML = res.result.q
                    e.innerHTML =  res.result.e
                    d.innerHTML =  res.result.d
                    fiN.innerHTML =  res.result.fiN
                    N.innerHTML =  res.result.N
                }
            })
            // res.catch(alert('Произошла невиданная ошибка, попробуйте позднее'))
        } else alert('Введите допустимое количество битов')

    }

    decipher(){
        let d = document.getElementById('d').value
        let N = document.getElementById('N').value
        let cryptogramm = document.getElementById('textCrypt').value

        let text = document.getElementById('textCrypt')

        if(!d || !N || !text){
            alert('Заполните все поля!')
        }
        else{
            let res = apiPos({'d': d, 'N': N, 'text': cryptogramm}, '/decipher')
            res.then(res => {
                if(res.error === 'error') alert('Ошибка расшифрования!')
                if(res.status === 'ok'){
                    text.innerHTML = res.text
                }
            })
        }
        
    }


    cipher(){
        let e = document.getElementById('e').value
        let N = document.getElementById('N').value
        let text = document.getElementById('text').value

        let cryptogramm = document.getElementById('textCrypt')
        console.log(e)

        if(!e || !N || !text){
            alert('Заполните все поля!')
        }
        else{
            let res = apiPos({'e': e, 'N': N, 'text': text}, '/cipher')
            res.then(res => {
                if(res.status === 'ok'){
                    cryptogramm.innerHTML = res.text
                }
            })
        }
        
    }
}

export default Form