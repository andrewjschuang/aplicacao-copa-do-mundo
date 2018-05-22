import psycopg2
import pandas as pd
import pandas.io.sql as psql
# CLASS TO CONNECT DB 
class Connection(object):
    def __init__(self,dbname='mydb', user='phillipe'):
        try:
            self.conn = psycopg2.connect(dbname=dbname, user=user)
            self.cursor = self.conn.cursor()
        except:
            print("Não foi possível se conectar ao Banco de Dados")
            raise
        # Variables used in more than a method
        self.authorized = False
        self.id_user = None
        self.email_user = None
        self.password_user = None
        self.name_user = None
        self.nationality = None
        # result = select(cursor, 'cities')
        # printResults(result)

    def close(self):
        self.cursor.close()
        self.conn.close()

    def login_user(self,email,password,condition=None):
        if condition:
            pass
        else:
        	#Check if email with the right password is valid
        	result = []
        	command = ('SELECT idpessoa,nomepessoa,nacionalidade FROM pessoa NATURAL JOIN torcedor WHERE email=%s AND senha=%s' % (email,password))
        	self.cursor.execute(command)
        	result = self.cursor.fetchall()
        	print(result)
        	# USER INFORMATION INSTANCE
        	if result != []:
        		self.authorized = True
        		self.id_user = result[0][0]
        		self.name_user = result[0][1]
        		self.nationality = result[0][2]
        		self.email_user = email[1:-1] #remove quots
        		self.password_user = password[1:-1] #remove quots

        	else:
        		self.authorized = False
        		self.id_user = None
        		self.name_user = None
        		self.nationality = None
        		self.email_user = None
        		self.password_user = None
        	return result
    # Try to register a new user, if a new email is given
    def registerSucess(self,name,password,email,nationality,condition=None):
        if condition:
            pass
        else:
            #IF email exists , return False
            command = ('SELECT email FROM  torcedor WHERE email=%s' % (email))
            self.cursor.execute(command)
            result = self.cursor.fetchall()
            print(result)
            if result != []:
                return False
            # If email not registered, choose a new idpessoa for the new user based on the existing idpessoa 
            command = ('SELECT max(idpessoa) FROM  pessoa' )
            self.cursor.execute(command)
            result = self.cursor.fetchall()
            idpessoa_new = result[0][0] + 1
            # Insert new person on pessoa
            command = ('INSERT INTO pessoa (idpessoa,nomepessoa,nacionalidade) VALUES (%s,%s,%s);' % (idpessoa_new,name,nationality))
            self.cursor.execute(command)
            # Commit the DB write
            self.conn.commit()
            #Insert new pessoa in torcedor
            command = ('INSERT INTO torcedor (idpessoa,email,senha) VALUES (%s,%s,%s);' % (idpessoa_new,email,password))
            self.cursor.execute(command)
            # Commit the DB write
            self.conn.commit()
            #Update instance
            self.name_user = name[1:-1] #remove quots
            self.nationality = nationality[1:-1] #remove quots
            self.email_user = email[1:-1] #remove quots
            self.password_user = password[1:-1] #remove quots
            return True


    def select(self, relation, condition=None):
        if condition:
            pass
        else:
            # For a pretty table html, make the querry with pandas api, then send result to server
            result = psql.read_sql('SELECT * FROM %s' % relation,self.conn)
            # OLD Version of querry without pretty tables
            """self.cursor.execute(command)
            return self.cursor.declare(),self.cursor.fetchall()"""
            return result

    def update_settings(self,name,nationality,email,password,condition =None):
    	if condition:
    		pass
    	else:
    		command = ('UPDATE pessoa SET nomepessoa=%s , nacionalidade=%s WHERE idpessoa=%s ;' % (name,nationality,self.id_user))
    		self.cursor.execute(command)
    		command = ('UPDATE torcedor SET email=%s , senha=%s WHERE idpessoa=%s ;' % (email,password,self.id_user))
    		self.cursor.execute(command)
    		self.conn.commit()
    		return True



    def printResults(self,results):
        for item in results:
            print(item)
