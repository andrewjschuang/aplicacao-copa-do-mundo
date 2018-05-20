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
        self.authorized = 0
        self.id_user = None
        
        # result = select(cursor, 'cities')
        # printResults(result)

    def close(self):
        self.cursor.close()
        self.conn.close()

    def login_user(self,email,password,condition=None):
        if condition:
            pass
        else:
            #command = ('SELECT * FROM torcedor \
            #            WHERE email=%sand senha=%s' % (email,password))
            command = ('SELECT nomepessoa FROM pessoa NATURAL JOIN torcedor WHERE email=%s AND senha=%s' % (email,password))
            self.cursor.execute(command)
            result = self.cursor.fetchall()
            print(result)
            return result

    def registerSucess(self,name,password,email,nationality,condition=None):
        if condition:
            pass
        else:
            command = ('SELECT email FROM  torcedor WHERE email=%s' % (email))
            self.cursor.execute(command)
            result = self.cursor.fetchall()
            print(result)
            if result != []:
                return False

            command = ('SELECT max(idpessoa) FROM  pessoa' )
            self.cursor.execute(command)
            result = self.cursor.fetchall()
            idpessoa_new = result[0][0] + 1
            command = ('INSERT INTO pessoa (idpessoa,nomepessoa,nacionalidade) VALUES (%s,%s,%s);' % (idpessoa_new,name,nationality))
            self.cursor.execute(command)
            self.conn.commit()
            
            command = ('INSERT INTO torcedor (idpessoa,email,senha) VALUES (%s,%s,%s);' % (idpessoa_new,email,password))
            self.cursor.execute(command)
            self.conn.commit()
            return True


    def select(self, relation, condition=None):
        if condition:
            pass
        else:
            result = psql.read_sql('SELECT * FROM %s' % relation,self.conn)
           
            """self.cursor.execute(command)
            return self.cursor.declare(),self.cursor.fetchall()"""
            return result

    def printResults(self,results):
        for item in results:
            print(item)
