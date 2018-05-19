from flask import Flask, render_template, request ,redirect , url_for
from flask_table import Table, Col
import database


app = Flask(__name__)
app.static_folder = "static"
connection = database.Connection(dbname='mydb', user='phillipe')
# Insert a " for the querry
def putsQuot(line):
	return "\'"+line+"\'"

@app.route('/', methods=['POST', 'GET'])
@app.route("/index.html", methods=['POST','GET'])
# Login With a email and password
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

	    #return '''<h1>USERNAME: {}</h1>'''.format(results[0][0])
	    return redirect(url_for('consulta'))

	elif request.method == 'POST' and  'register' in request.form:
		 return redirect(url_for('registra'))

	else:
	    return render_template('index.html')
	    
@app.route('/registra',methods=['POST','GET'])
def registra():
	if request.method == 'POST' and "submit" in request.form:
		name = request.form.get('name')
		nationality = request.form.get('nationality')
		email = request.form.get('email')
		password = request.form.get('password')

		email=putsQuot(email)
		password= putsQuot(password)
		nationality = putsQuot(nationality)
		name = putsQuot(name)

		if(connection.registerSucess(name,password,email,nationality)):
			return redirect(url_for('login'))
		else:
			return render_template(('form-register.html'),already_exists="EMAIL ALREADY REGISTERED")


	return render_template('form-register.html')

@app.route('/consulta', methods=['POST', 'GET'])
def consulta():

	if request.method == 'POST':
	    query = request.form.get('query')
	    results = connection.select(query)

	    return render_template('form.html', results=results)
	return render_template('form.html',)

app.run(debug=True, use_reloader=True)
