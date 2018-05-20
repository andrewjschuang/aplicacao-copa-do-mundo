from flask import Flask, render_template, request ,redirect , url_for
import pandas as pd
import database


app = Flask(__name__)
app.static_folder = "static"
connection = database.Connection(dbname='mydb', user='phillipe')
# Insert a " in the begin and end of querry
def putsQuot(line):
	return "\'"+line+"\'"

@app.route('/', methods=['POST', 'GET'])
@app.route("/index.html", methods=['POST','GET'])
# Login With a email and password
def login():
	if request.method == 'POST' and "login" in request.form :  #this block is only entered when the form is submitted
		# Reques user email and password for check registers in DB
	    email = request.form.get('user_email')
	    password = request.form.get('password')
	    email="\'"+email+"\'"
	    password="\'"+password+"\'"
	    results = connection.login_user(email,password)
	    #IF Regsiter not found return a HTML with ACESS DENIED
	    if(results == []):
	        return '''<h1>ACESS DENIED</h1>
	        		  <h1>EMAIL AND/OR PASSWORD INCORRECT</h1>'''

	    #return '''<h1>USERNAME: {}</h1>'''.format(results[0][0])
	    # IF Register found goes to  page consulta
	    return redirect(url_for('consulta'))
	# IF botton register was click goes to page registra
	elif request.method == 'POST' and  'register' in request.form:
		 return redirect(url_for('registra'))

	else:
		# If nothing was actioned render the index.html
	    return render_template('index.html')
# Page registra
@app.route('/registra',methods=['POST','GET'])
def registra():
	# if all field of forms was filled querry try to insert new user in DB
	if request.method == 'POST' and "submit" in request.form:
		name = request.form.get('name')
		nationality = request.form.get('nationality')
		email = request.form.get('email')
		password = request.form.get('password')

		email=putsQuot(email)
		password= putsQuot(password)
		nationality = putsQuot(nationality)
		name = putsQuot(name)
		# IF email not in BD register new user , then goes to page login
		if(connection.registerSucess(name,password,email,nationality)):
			return redirect(url_for('login'))
		else:
			# Else print EMAIL ALREADY REGISTERED in the header of the page
			return render_template(('form-register.html'),already_exists="EMAIL ALREADY REGISTERED")

	# If nothing was actioned render the form-register.html
	return render_template('form-register.html')
# Page consulta
@app.route('/consulta', methods=['POST', 'GET'])
def consulta():
	# Make a querry in DB
	if request.method == 'POST':
	    query = request.form.get('query')
	    df = connection.select(query)
	    # Return result Table render in html
	    return render_template('form.html',name='RESULTADO',data = df.to_html())
	# If nothing was actioned render the form.html
	return render_template('form.html',)
# Run app
app.run(debug=True, use_reloader=True)
