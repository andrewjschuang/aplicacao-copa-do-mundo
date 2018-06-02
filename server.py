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
        return render_template('login_update.html',message="PLEASE INSERT YOUR LOGIN TO CHANGE YOUR CONFIGURATIONS")

    # Make a update_settings in DB with idpessoa as id_user
    if request.method == 'POST' and 'update' in request.form:
        blank_field = 0
        name = putsQuot(request.form.get('name'))
        if name[1:-1] == "" or name[1:-1].isspace(): # name without quots
            blank_field = blank_field +1
            name = putsQuot(connection.name_user)
        nationality = putsQuot(request.form.get('nationality'))
        if nationality[1:-1] == "" or nationality[1:-1].isspace(): # nationality without quots
            blank_field = blank_field +1
            nationality = putsQuot(connection.nationality)
        email = putsQuot(request.form.get('email'))
        if email[1:-1] == "" or email[1:-1].isspace(): # email without quots
            blank_field = blank_field +1
            email = putsQuot(connection.email_user)
        password = putsQuot(request.form.get('password'))
        if password[1:-1] == "" or password[1:-1].isspace(): # password without quots
            blank_field = blank_field +1
            password = putsQuot(connection.password_user)

        if(blank_field<4): # IF USER TYPE IN SOME FIELD
            if(connection.update_settings(name,nationality,email,password)):
                return redirect(url_for('consulta'))

    # If nothing was actioned render the form.
    print(connection.nationality)
    return render_template('configuracao.html',username=connection.name_user,nationality=connection.nationality,email=connection.email_user,password=connection.password_user)

# Page shopping
@app.route('/shopping', methods=['POST', 'GET'])
def shopping():
    return render_template('shopping.html')

# Page contratatradutor
@app.route('/shopping/contratatradutor', methods=['POST', 'GET'])
def contratatradutor():
    ## Force user to be logged
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
                df = connection.translators()
                if df is None:
                    return render_template('contratatradutor.html',translators_querry="NOBODY IS AVAILABLE")
                else:
                    return render_template('contratatradutor.html',data = df.to_html())
        return render_template('login_update.html',message="PLEASE INSERT YOUR LOGIN TO MAKE ANY TRANSATION")

    if request.method == 'POST' and 'translator' in request.form:
        # Verify if the user is logged
        idtradutor = request.form.get('translator')
        idtradutor_str = str(idtradutor)
        if idtradutor!= None and idtradutor_str.isnumeric():
            print(idtradutor)
            # Buy Tickets with idtradutor logged
            idtradutor_exist,idtradutor_disponivel = connection.hireTranslator(idtradutor)
            print(idtradutor_exist,idtradutor_disponivel)
            if(idtradutor_exist and  idtradutor_disponivel):
                return render_template('contratatradutor.html',message="TRANSATION SUCCESS")
            elif(not idtradutor_exist):
                return render_template('contratatradutor.html',message="idpessoa NOT VALID")
            else:
                return render_template('contratatradutor.html',message="TRANSLATOR NOT AVAILABLE")
    else:
        df = connection.translators()
        if df is None:
            return render_template('contratatradutor.html',translators_querry="NOBODY IS AVAILABLE")
        else:
            return render_template('contratatradutor.html',data = df.to_html())

# Page contrataguia
@app.route('/shopping/contrataguia', methods=['POST', 'GET'])
def contrataguia():
    ## Force user to be logged
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
                df = connection.guides()
                if df is None:
                    return render_template('contrataguia.html',translators_querry="NOBODY IS AVAILABLE")
                else:
                    return render_template('contrataguia.html',data = df.to_html())
        return render_template('login_update.html',message="PLEASE INSERT YOUR LOGIN TO MAKE ANY TRANSATION")

    if request.method == 'POST' and 'find_guide' in request.form:
        # Verify if the user is logged
        idguia = request.form.get('find_guide')
        idguia_str = str(idguia)
        if idguia!= None and idguia_str.isnumeric():
            print(idguia)
            # Buy Tickets with idguia logged
            idguia_exist,idguia_disponivel = connection.contatcGuide(idguia)
            print(idguia_exist,idguia_disponivel)
            if(idguia_exist and  idguia_disponivel):
                return render_template('contrataguia.html',message="TRANSATION SUCCESS")
            elif(not idguia_exist):
                return render_template('contrataguia.html',message="idpessoa NOT VALID")
            else:
                return render_template('contrataguia.html',message="GUIDE NOT AVAILABLE")

    else:
        df = connection.guides()
        if df is None:
            return render_template('contrataguia.html',translators_querry="NOBODY IS AVAILABLE")
        else:
            return render_template('contrataguia.html',data = df.to_html())
# Page tickets
@app.route('/shopping/tickets', methods=['POST', 'GET'])
def tickets():
    ## Force user to be logged
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
                df = connection.matches()
                if df is None:
                    return render_template('tickets.html',translators_querry="NO TICKETS AVAILABLE")
                else:
                    return render_template('tickets.html',data = df.to_html())
        return render_template('login_update.html',message="PLEASE INSERT YOUR LOGIN TO MAKE ANY TRANSATION")



    if request.method == 'POST' and 'buy-tickets' in request.form:
        # Verify if the user is logged
        codpartida = request.form.get('buy-tickets')
        codpartida_str = str(codpartida)
        if codpartida!= None and codpartida_str.isnumeric():
            print(codpartida)
            # Buy Tickets with idpessoa logged
            codpartida_exist,new_ticket = connection.buyTickets(codpartida)
            print(codpartida_exist,new_ticket)
            if(codpartida_exist and  new_ticket):
                return render_template('tickets.html',message="TRANSATION SUCCESS")
            elif(not codpartida_exist):
                return render_template('tickets.html',message="codpartida NOT VALID")
            else:
                return render_template('tickets.html',message="TICKET ALREADY BOUGHT")

    else:
        df = connection.matches()
        if df is None:
            return render_template('tickets.html',translators_querry="NO TICKETS AVAILABLE")
        else:
            return render_template('tickets.html',data = df.to_html())

# Page matches
@app.route('/partidas', methods=['GET','POST'])
def partidas():
    # Search all matches
    df = connection.matches(past=True)
    df.insert(3, 'Increment goal', '<button onclick="increment1(this)">Increment</button>', allow_duplicates=True)
    df.insert(5, 'Increment goal', '<button onclick="increment2(this)">Increment</button>', allow_duplicates=True)
    df.insert(df.shape[-1], 'Modify score', '<button onclick="update_score(this)">Modify</button>')
    df.sort_values(['codpartida'], inplace=True)

    # Return result Table render in html
    return render_template('partidas.html', data=df.to_html(index=False,escape=False))

@app.route('/increment', methods=['GET','POST'])
def increment():
    golselecao = request.args.get('country')
    codpartida = int(request.args.get('codpartida'))
    df = connection.incrementGoal(golselecao, codpartida)
    return redirect(url_for('partidas'))

@app.route('/modifyscore', methods=['GET', 'POST'])
def modifyscore():
    codpartida = request.args.get('codpartida')
    selecao1 = request.args.get('selecao1')
    selecao2 = request.args.get('selecao2')
    goal1 = request.args.get('goal1')
    goal2 = request.args.get('goal2')
    return render_template('modificar_placar.html', codpartida=codpartida, selecao1=selecao1, selecao2=selecao2, goal1=goal1, goal2=goal2)

@app.route('/modifyscoreaux', methods=['POST'])
def modifyscoreaux():
    codpartida = request.form['codpartida']
    goal1 = request.form['goal1']
    goal2 = request.form['goal2']
    df = connection.modifyScore(goal1, goal2, codpartida)
    return redirect(url_for('partidas'))

# Run app
app.run(debug=True, use_reloader=True)
