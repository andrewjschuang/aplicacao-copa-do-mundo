from flask import Flask, render_template, request
from database import *

app = Flask(__name__)

conn, cursor = init()

@app.route('/', methods=['POST', 'GET'])
@app.route('/consulta', methods=['POST', 'GET'])
def consulta(last_selected=None):
    if request.method == 'POST':
        query = request.form.get('query')
        # results = select(cursor, query)
        results = query
        return render_template('form.html', results=results)
    return render_template('form.html')


app.run(debug=True, use_reloader=True)
