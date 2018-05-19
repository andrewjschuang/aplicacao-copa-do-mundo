import psycopg2
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

    def select(self, relation, condition=None):
        if condition:
            pass
        else:
            command = ('SELECT * FROM %s' % relation)
        self.cursor.execute(command)
        return self.cursor.fetchall()

    def printResults(self,results):
        for item in results:
            print(item)
