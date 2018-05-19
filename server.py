from flask import Flask, render_template, request
import database

app = Flask(__name__)
app.static_folder = "static"
connection = database.Connection(dbname='mydb', user='phillipe')

@app.route('/', methods=['POST', 'GET'])
@app.route("/index.html", methods=['POST','GET'])
def login():
    if request.method == 'POST' and "login" in request.form :  #this block is only entered when the form is submitted

        email = request.form.get('user_email')
        password = request.form.get('password')
        email="\'"+email+"\'"
        password="\'"+password+"\'"
        results = connection.login_user(email,password)

        if(results == []):
	        return '''<h1>ACESS DENIED</h1>
	        		  <h1>EMAIL AND/OR PASSWORD INCORRECT</h1>'''

        return '''<h1>USERNAME: {}</h1>'''.format(results[0][0])

    else:

        return render_template('index.html')
@app.route('/consulta', methods=['POST', 'GET'])
def consulta():
    if request.method == 'POST':
        query = request.form.get('query')
        results = connection.select(query)
        return render_template('form.html', results=results)
    return render_template('form.html')

app.run(debug=True, use_reloader=True)
