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
            self.name_user = name[1:-1] #remove quots
            self.nationality = nationality[1:-1] #remove quots
            self.email_user = email[1:-1] #remove quots
            self.password_user = password[1:-1] #remove quots
            return True

    def translators(self,condition = None):
        if condition:
            pass
        else:
             # Query returns the names of  guides
             query = 'SELECT idpessoa, nomepessoa,disponibilidade,idioma,valorhora \
                      FROM tradutor NATURAL JOIN pessoa\
                      WHERE tradutor.idpessoa = pessoa.idpessoa ;' ;
             result = psql.read_sql(query,self.conn)
             return result

    def hireTranslator(self,idtranslator,condition=None):
        if condition:
            pass
        else:
             # VERIFY IF translator EXISTS
            command = ('SELECT idpessoa FROM tradutor WHERE idpessoa=%s ;' % idtranslator)
            self.cursor.execute(command)
            idtranslator_exists = self.cursor.fetchall()
             # VERIFY IF user has already caontacted a guide
            command = ('SELECT idtorcedor FROM contrata WHERE idtorcedor=%s ;' % self.id_user)
            self.cursor.execute(command)
            already_contacted = self.cursor.fetchall()

            if idtranslator_exists != [] and already_contacted == []:
                command = ('INSERT INTO  contrata (idtradutor,idtorcedor) VALUES (%s ,%s);' % (idtranslator,self.id_user) )
                self.cursor.execute(command)
                command = ('UPDATE tradutor SET disponibilidade=FALSE WHERE idpessoa=%s;' % (idtranslator) )
                self.cursor.execute(command)
                self.conn.commit()
                return True,True #Operation success
            elif idtranslator_exists == []:
                return False,True # Failed finding translator
            elif already_contacted != []:
                return True,False # Failed, traslator already hired
            return False,False # Failed, exception

    def contatcGuide(self,idguia,condition = None):
        if condition:
            pass
        else:
            # VERIFY IF guide EXISTS
            command = ('SELECT idpessoa FROM guia_voluntario WHERE idpessoa=%s ;' % idguia)
            self.cursor.execute(command)
            idguia_exists = self.cursor.fetchall()
             # VERIFY IF user has already caontacted a guide
            command = ('SELECT idtorcedor FROM ajuda WHERE idtorcedor=%s ;' % self.id_user)
            self.cursor.execute(command)
            already_contacted = self.cursor.fetchall()

            if idguia_exists != [] and already_contacted == []:
                command = ('INSERT INTO  ajuda (idguia,idtorcedor) VALUES (%s ,%s);' % (idguia,self.id_user) )
                self.cursor.execute(command)
                command = ('UPDATE guia_voluntario SET disponibilidade=FALSE WHERE idpessoa=%s;' % (idguia) )
                self.cursor.execute(command)
                self.conn.commit()
                return True,True
            elif idguia_exists == []:
                return False,True
            elif already_contacted != []:
                return True,False
            return False,False

    def guides(self,condition =None):
        if condition:
            pass
        else:
             # Query returns the names of  guides
             query = 'SELECT idpessoa, nomepessoa,disponibilidade,nomecidade \
                      FROM guia_voluntario NATURAL JOIN pessoa\
                      WHERE guia_voluntario.idpessoa = pessoa.idpessoa ;' ;
             result = psql.read_sql(query,self.conn)
             return result


    def matches(self, condition = None):
        if condition:
            pass
        else:
            # Query returns the names of teams that will play in the same match at a data and location 
            query = 'SELECT codpartida,selecao1,selecao2,datapartida,nomecidade \
                    FROM \
                   ( SELECT datapartida,idselecao2,selecao1,nomecidade,codpartida FROM partida NATURAL JOIN selecao AS sel1(idselecao1,selecao1))\
                     AS partida_selecao JOIN selecao AS sel2(idselecao2,selecao2) ON partida_selecao.idselecao2=sel2.idselecao2 ;'
            result = psql.read_sql( query,self.conn)
            return result
    def buyTickets(self, codpartida, condition = None):
        if condition:
            pass
        else:
            # VERIFY IF codpartida EXISTS
            command = ('SELECT codpartida FROM partida WHERE codpartida=%s ;' % codpartida)
            self.cursor.execute(command)
            codpartida_exists = self.cursor.fetchall()
             # VERIFY IF user has bought already the same ticket
            command = ('SELECT codpartida FROM compraingresso WHERE codpartida=%s ;' % codpartida)
            self.cursor.execute(command)
            already_bought = self.cursor.fetchall()

            if codpartida_exists != [] and already_bought == []:
                command = ('INSERT INTO  compraingresso (idpessoa,codpartida) VALUES (%s ,%s);' % (self.id_user,codpartida))
                self.cursor.execute(command)
                self.conn.commit()
                return True,True
            elif codpartida_exists == []:
                return False,True
            elif already_bought != []:
                return True,False
            return False,False

            
    def printResults(self,results):
        for item in results:
            print(item)
