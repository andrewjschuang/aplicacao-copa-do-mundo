from flask import Flask, render_template, request
import database

app = Flask(__name__)

conn, cursor = database.init(dbname='newdb', user='andrewjschuang')

@app.route('/', methods=['POST', 'GET'])
@app.route('/consulta', methods=['POST', 'GET'])
def consulta():
    if request.method == 'POST':
        query = request.form.get('query')
        results = database.select(cursor, query)
        return render_template('form.html', results=results)
    return render_template('form.html')

app.run(debug=True, use_reloader=True)
