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
	connection.id_user = None #Inicialize id_user in login page
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

# Page configuracao
@app.route('/configuracao', methods=['POST', 'GET'])
def configuracao():
	if connection.id_user == None:
		#Login Settings
		if request.method == 'POST' and "login" in request.form :  #this block is only entered when the form is submitted
			# Reques user email and password for check registers in DB
		    email = putsQuot(request.form.get('user_email'))
		    password = putsQuot(request.form.get('password'))
		    results = connection.login_user(email,password)
		    #IF Regsiter not found return a HTML with ACESS DENIED
		    if(results == []):
		        return '''<h1>ACESS DENIED</h1>
		        		  <h1>EMAIL AND/OR PASSWORD INCORRECT</h1>'''
		    # If User Found goes to Settings
		    else:
		    	return render_template('configuracao.html',username=connection.name_user,nationality=connection.nationality,email=connection.email_user,password=connection.password_user)
		return render_template('login_update.html')

	# Make a update_settings in DB with idpessoa as id_user
	if request.method == 'POST' and 'update' in request.form:
		blank_field = 0
		name = putsQuot(request.form.get('name'))
		if name[1:-1] == "": # name without quots
			blank_field = blank_field +1
			name = putsQuot(connection.name_user)
		nationality = putsQuot(request.form.get('nationality'))
		if nationality[1:-1] == "": # nationality without quots
			blank_field = blank_field +1
			nationality = putsQuot(connection.nationality)
		email = putsQuot(request.form.get('email'))
		if email[1:-1] == "": # email without quots
			blank_field = blank_field +1
			email = putsQuot(connection.email_user)
		password = putsQuot(request.form.get('password'))
		if password[1:-1] == "": # password without quots
			blank_field = blank_field +1
			password = putsQuot(connection.password_user)

		if(blank_field<4): # IF USER TYPE IN SOME FIELD
			if(connection.update_settings(name,nationality,email,password)):
				return redirect(url_for('login'))
	  
	# If nothing was actioned render the form.
	print(connection.nationality)
	return render_template('configuracao.html',username=connection.name_user,nationality=connection.nationality,email=connection.email_user,password=connection.password_user)

# Run app
app.run(debug=True, use_reloader=True)
