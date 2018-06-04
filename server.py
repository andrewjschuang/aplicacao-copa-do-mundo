from flask import Flask, render_template, request ,redirect , url_for
import pandas as pd
import database

app = Flask(__name__)
app.static_folder = "static"
connection = database.Connection(dbname='mydb', user='postgres')

# Insert a " in the begin and end of querry
def puts_quote(line):
    return "\'"+line+"\'"
# puts_quote()

@app.route('/', methods=['POST', 'GET'])
@app.route("/index.html", methods=['POST','GET'])
def login():
    '''Login with an email and a password'''

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
# login()

@app.route('/registra',methods=['POST','GET'])
def registra():
    '''Page registra'''
    # if all field of forms was filled querry try to insert new user in DB
    if request.method == 'POST' and "submit" in request.form:
        name = request.form.get('name')
        nationality = request.form.get('nationality')
        email = request.form.get('email')
        password = request.form.get('password')

        email=puts_quote(email)
        password= puts_quote(password)
        nationality = puts_quote(nationality)
        name = puts_quote(name)
        # IF email not in BD register new user , then goes to page login
        if(connection.register_success(name,password,email,nationality)):
            return redirect(url_for('login'))
        else:
            # Else print EMAIL ALREADY REGISTERED in the header of the page
            return render_template(('form-register.html'),already_exists="EMAIL ALREADY REGISTERED")

    # If nothing was actioned render the form-register.html
    return render_template('form-register.html')
# registra()

@app.route('/consulta', methods=['POST', 'GET'])
def consulta():
    '''Page consulta'''

    # Make a querry in DB
    # if 'query-gols' in request.form:
    #     df = connection.select('query_cidades_jogadores')
    #     return render_template('form.html',name='RESULTADO',data = df.to_html())
    if 'query_viagem_jogadores' in request.form:
        args = ["\'"+request.form.get('jogador1')+"\'", "\'"+request.form.get('jogador2')+"\'"]
        df = connection.select('query_viagem_jogadores', args=args)
        return render_template('form.html', name='RESULTADO', data = df.to_html())

    elif 'query_cidades_jogadores' in request.form:
        df = connection.select('query_cidades_jogadores')
        return render_template('form.html',name='RESULTADO',data = df.to_html())

    elif 'query_hoteis_selecao' in request.form:
        args = ["\'"+request.form.get('selecao')+"\'"]
        df = connection.select('query_hoteis_selecao', args=args)
        return render_template('form.html',name='RESULTADO',data = df.to_html())

    elif "query_guias" in request.form:
        args = ["\'"+request.form.get('id_torcedor')+"\'"]
        df = connection.select('query_guias', args=args)
        return render_template('form.html',name='RESULTADO',data = df.to_html())

    elif "query_comissao" in request.form:
        df = connection.select('query_comissao')
        return render_template('form.html',name='RESULTADO',data = df.to_html())

    elif "query_jogador_gols" in request.form:
        args = ["\'"+request.form.get('posicao')+"\'", "\'"+request.form.get('n_gols')+"\'"]
        df = connection.select('query_jogador_gols', args=args)
        return render_template('form.html',name='RESULTADO',data = df.to_html())

    elif 'query_eventos' in request.form:
        df = connection.select('query_eventos')
        return render_template('form.html',name='RESULTADO',data = df.to_html())

    elif 'whole table' in request.form:
    # if request.method == 'POST':
        print('whole table asked!')
        query = request.form.get('query')
        df = connection.select(query)
        # Return result Table render in html
        return render_template('form.html',name='RESULTADO',data = df.to_html())

    # If nothing was actioned render the form.html
    return render_template('form.html',)
# consulta()

@app.route('/configuracao', methods=['POST', 'GET'])
def configuracao():
    '''Page configuracao'''
    if connection.id_user == None:
        #Login Settings
        if request.method == 'POST' and "login" in request.form :  #this block is only entered when the form is submitted
            # Reques user email and password for check registers in DB
            email = puts_quote(request.form.get('user_email'))
            password = puts_quote(request.form.get('password'))
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
        name = puts_quote(request.form.get('name'))
        if name[1:-1] == "" or name[1:-1].isspace(): # name without quots
            blank_field = blank_field +1
            name = puts_quote(connection.name_user)
        nationality = puts_quote(request.form.get('nationality'))
        if nationality[1:-1] == "" or nationality[1:-1].isspace(): # nationality without quots
            blank_field = blank_field +1
            nationality = puts_quote(connection.nationality)
        email = puts_quote(request.form.get('email'))
        if email[1:-1] == "" or email[1:-1].isspace(): # email without quots
            blank_field = blank_field +1
            email = puts_quote(connection.email_user)
        password = puts_quote(request.form.get('password'))
        if password[1:-1] == "" or password[1:-1].isspace(): # password without quots
            blank_field = blank_field +1
            password = puts_quote(connection.password_user)

        if(blank_field<4): # IF USER TYPE IN SOME FIELD
            if(connection.update_settings(name,nationality,email,password)):
                return redirect(url_for('consulta'))

    # If nothing was actioned render the form.
    print(connection.nationality)
    return render_template('configuracao.html',username=connection.name_user,nationality=connection.nationality,email=connection.email_user,password=connection.password_user)
# configuracao()

@app.route('/shopping', methods=['POST', 'GET'])
def shopping():
    '''Page shopping'''
    return render_template('shopping.html')
# shopping()

@app.route('/shopping/contrata_tradutor', methods=['POST', 'GET'])
def contrata_tradutor():
    '''Page contrata_tradutor'''

    ## Force user to be logged
    if connection.id_user == None:
        #Login Settings
        if request.method == 'POST' and "login" in request.form :  #this block is only entered when the form is submitted
            # Reques user email and password for check registers in DB
            email = puts_quote(request.form.get('user_email'))
            password = puts_quote(request.form.get('password'))
            results = connection.login_user(email,password)
            #IF Regsiter not found return a HTML with ACESS DENIED
            if(results == []):
                return '''<h1>ACESS DENIED</h1>
                        <h1>EMAIL AND/OR PASSWORD INCORRECT</h1>'''
            # If User Found goes to Settings
            else:
                df = connection.translators()
                if df is None:
                    return render_template('contrata_tradutor.html',translators_querry="NOBODY IS AVAILABLE")
                else:
                    return render_template('contrata_tradutor.html',data = df.to_html())
        return render_template('login_update.html',message="PLEASE INSERT YOUR LOGIN TO MAKE ANY TRANSATION")

    if request.method == 'POST' and 'translator' in request.form:
        # Verify if the user is logged
        idtradutor = request.form.get('translator')
        idtradutor_str = str(idtradutor)
        if idtradutor!= None and idtradutor_str.isnumeric():
            print(idtradutor)
            # Buy Tickets with idtradutor logged
            idtradutor_exist,idtradutor_disponivel = connection.hire_translator(idtradutor)
            print(idtradutor_exist,idtradutor_disponivel)
            if(idtradutor_exist and  idtradutor_disponivel):
                return render_template('contrata_tradutor.html',message="TRANSATION SUCCESS")
            elif(not idtradutor_exist):
                return render_template('contrata_tradutor.html',message="idpessoa NOT VALID")
            else:
                return render_template('contrata_tradutor.html',message="TRANSLATOR NOT AVAILABLE")
    else:
        df = connection.translators()
        if df is None:
            return render_template('contrata_tradutor.html',translators_querry="NOBODY IS AVAILABLE")
        else:
            return render_template('contrata_tradutor.html',data = df.to_html())
# contrata_tradutor()

@app.route('/shopping/contrata_guia', methods=['POST', 'GET'])
def contrata_guia():
    '''Page contrata_guia'''

    ## Force user to be logged
    if connection.id_user == None:
        #Login Settings
        if request.method == 'POST' and "login" in request.form :  #this block is only entered when the form is submitted
            # Reques user email and password for check registers in DB
            email = puts_quote(request.form.get('user_email'))
            password = puts_quote(request.form.get('password'))
            results = connection.login_user(email,password)
            #IF Regsiter not found return a HTML with ACESS DENIED
            if(results == []):
                return '''<h1>ACESS DENIED</h1>
                        <h1>EMAIL AND/OR PASSWORD INCORRECT</h1>'''
            # If User Found goes to Settings
            else:
                df = connection.guides()
                if df is None:
                    return render_template('contrata_guia.html',translators_querry="NOBODY IS AVAILABLE")
                else:
                    return render_template('contrata_guia.html',data = df.to_html())
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
                return render_template('contrata_guia.html',message="TRANSATION SUCCESS")
            elif(not idguia_exist):
                return render_template('contrata_guia.html',message="idpessoa NOT VALID")
            else:
                return render_template('contrata_guia.html',message="GUIDE NOT AVAILABLE")

    else:
        df = connection.guides()
        if df is None:
            return render_template('contrata_guia.html',translators_querry="NOBODY IS AVAILABLE")
        else:
            return render_template('contrata_guia.html',data = df.to_html())
# contrata_guia()

@app.route('/shopping/tickets', methods=['POST', 'GET'])
def tickets():
    '''Page tickets'''

    ## Force user to be logged
    if connection.id_user == None:
        #Login Settings
        if request.method == 'POST' and "login" in request.form :  #this block is only entered when the form is submitted
            # Reques user email and password for check registers in DB
            email = puts_quote(request.form.get('user_email'))
            password = puts_quote(request.form.get('password'))
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
            codpartida_exist,new_ticket = connection.buy_tickets(codpartida)
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
# tickets()

@app.route('/partidas', methods=['GET','POST'])
def partidas():
    '''Page partidas'''
    # Search all matches
    df = connection.matches(past=True)
    df.insert(3, 'Increment goal', '<button onclick="increment1(this)">Increment</button>', allow_duplicates=True)
    df.insert(5, 'Increment goal', '<button onclick="increment2(this)">Increment</button>', allow_duplicates=True)
    df.insert(df.shape[-1], 'Modify score', '<button onclick="update_score(this)">Modify</button>')
    df.sort_values(['codpartida'], inplace=True)

    # Return result Table render in html
    return render_template('partidas.html', data=df.to_html(index=False,escape=False))
# partidas()

@app.route('/increment', methods=['GET','POST'])
def increment():
    golselecao = request.args.get('country')
    codpartida = int(request.args.get('codpartida'))
    df = connection.increment_goal(golselecao, codpartida)
    return redirect(url_for('partidas'))
# increment()

@app.route('/modify_score', methods=['GET', 'POST'])
def modify_score():
    codpartida = request.args.get('codpartida')
    selecao1 = request.args.get('selecao1')
    selecao2 = request.args.get('selecao2')
    goal1 = request.args.get('goal1')
    goal2 = request.args.get('goal2')
    return render_template('modificar_placar.html', codpartida=codpartida, selecao1=selecao1, selecao2=selecao2, goal1=goal1, goal2=goal2)
#modify_score()

@app.route('/modify_score_aux', methods=['POST'])
def modify_score_aux():
    codpartida = request.form['codpartida']
    goal1 = request.form['goal1']
    goal2 = request.form['goal2']
    df = connection.modify_score(goal1, goal2, codpartida)
    return redirect(url_for('partidas'))
# modify_score_aux()

# Run app
app.run(debug=True, use_reloader=True)
