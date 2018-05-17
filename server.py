from flask import Flask

app = Flask(__name__)

@app.route('/')
@app.route('/consulta')
def consulta():
    return 'Pagina de consulta'

@app.route('/resultado')
def resultado():
    return 'Resultado da consulta'

app.run(debug=True, use_reloader=True)
