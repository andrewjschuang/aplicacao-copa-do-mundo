import psycopg2
import pandas as pd
import pandas.io.sql as psql
# CLASS TO CONNECT DB
class Connection(object):

    def __init__(self,dbname='mydb', user='postgres'):
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
    # __init__()

    def close(self):
        self.cursor.close()
        self.conn.close()
    # close()

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
    # login_user()

    def register_success(self,name,password,email,nationality,condition=None):
        '''Try to register a new user if a new email is given'''
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
    # register_success()

    def select_nacionalidade(self):
        sql = "SELECT DISTINCT nacionalidade FROM pessoa"
        result = psql.read_sql(sql,self.conn)
        return result

    def select_partidas(self):
        sql = """
                SELECT DISTINCT codpartida, selecao1, selecao2, nomecidade, datapartida
                FROM   (
                 SELECT * FROM (
                  SELECT codpartida,nomecidade,idselecao1,idselecao2,selecao1, datapartida
                  FROM partida NATURAL JOIN selecao as sel1(idselecao1,selecao1)
                 )
                 AS partida_sel1 NATURAL JOIN selecao AS sel2(idselecao2,selecao2)
                ) AS partidas;
            """
        result = psql.read_sql(sql,self.conn)
        return result


    def select(self, query, args=[], condition=None):
        if condition:
            pass
        else:
            if query=="query_cidades_jogadores":
                nacionalidade = args[0]
                # sql = "select distinct nomecidade from partida join membro_selecao on \
                #         idselecao=idselecao or idselecao=idselecao2;"
                sql = """
                        SELECT DISTINCT nomecidade
                        FROM partida, membro_selecao, pessoa
                        WHERE (idselecao = idselecao1 OR idselecao = idselecao2)
                        AND membro_selecao.idpessoa = pessoa.idpessoa
                        AND pessoa.nacionalidade ="""+ nacionalidade + """ ;
                        """
                result = psql.read_sql(sql,self.conn)

            elif query=="query_eventos":
                codpartida = args[0]
                sql = """select nomeevento, dataevento
                        from evento,partida
                        where partida.codpartida="""+ codpartida +"""
                        and partida.nomecidade = evento.nomecidade
                        and dataevento <> datapartida
                        and to_char(partida.datapartida,'DD') = to_char(evento.dataevento,'DD') ;"""
                result = psql.read_sql(sql,self.conn)

            elif query == 'query_viagem_jogadores':
                jogador1, jogador2 = args
                if jogador2 == '':
                    jogador2 = jogador1
                sql = """SELECT *  FROM (
                             SELECT * FROM (
                              SELECT nomecidade,datapartida FROM partida WHERE
                              idselecao1 =(
                                 SELECT idselecao FROM membro_selecao WHERE
                                 idpessoa =(
                                    SELECT idpessoa FROM pessoa WHERE
                                    nomepessoa =""" + jogador1 + """
                                 )
                              )
                              OR idselecao2 =(
                                SELECT idselecao FROM membro_selecao WHERE
                                 idpessoa =(
                                    SELECT idpessoa FROM pessoa WHERE
                                    nomepessoa = """ + jogador1 + """
                                 )
                              ) ) AS cidadeJogador1(nomeorigem,datapartida1)  JOIN

                              (SELECT nomecidade,datapartida FROM partida WHERE
                              idselecao1 =(
                                 SELECT idselecao FROM membro_selecao WHERE
                                 idpessoa =(
                                    SELECT idpessoa FROM pessoa WHERE
                                    nomepessoa = """ + jogador2 + """
                                 )
                              )
                              OR idselecao2 =(
                                SELECT idselecao FROM membro_selecao WHERE
                                 idpessoa =(
                                    SELECT idpessoa FROM pessoa WHERE
                                    nomepessoa = """ + jogador2 + """
                                 )
                              ) ) AS cidadeJogador2(nomedestino,datapartida2)
                                ON cidadeJogador1.datapartida1 < cidadeJogador2.datapartida2)
                              AS cidadesProvaveis NATURAL JOIN viagem
                              WHERE dataviagem BETWEEN datapartida1 AND datapartida2 ;
                            """
                result = psql.read_sql(sql,self.conn)

            elif query == 'query_hoteis_selecao':
                selecao = args[0]
                sql = """SELECT nomehotel, hotel.nomecidade, valordiaria, disponivel FROM   (
                     SELECT * FROM (
                      SELECT nomecidade,idselecao1,idselecao2,selecao1
                      FROM partida NATURAL JOIN selecao as sel1(idselecao1,selecao1)
                     )
                     AS partida_sel1 NATURAL JOIN selecao AS sel2(idselecao2,selecao2)
                    )
                    AS selecoes_da_partida JOIN hotel ON hotel.nomecidade = selecoes_da_partida.nomecidade
                    WHERE selecao1="""+ selecao +"""  OR selecao2= """+ selecao +""" ;"""
                result = psql.read_sql(sql,self.conn)

            elif query=='query_guias':
                id_torcedor = self.id_user
                if id_torcedor is None:
                    id_torcedor=10000000
                sql = """SELECT * FROM (
                         SELECT idguia  FROM  (
                          SELECT codevento,nomecidade,idpessoa FROM
                           guia_voluntario NATURAL JOIN evento
                           WHERE guia_voluntario.disponibilidade = true
                          )
                          AS guiasDisponiveisNoEvento(codevento,nomecidade,idguia)
                          NATURAL JOIN interesse WHERE idpessoa=""" + str(id_torcedor) + """
                        )
                        AS guiasDisponiveisDeInteresseDoTorcedor(idpessoa) NATURAL JOIN pessoa;"""
                result = psql.read_sql(sql,self.conn)

            elif query=='query_comissao':
                pais = args[0]
                # sql = """select nomepessoa, numeroparticipacoescopa,funcaotecnica from pessoa
                #         inner join membro_selecao on membro_selecao.idpessoa = pessoa.idpessoa
                #         where funcaotecnica is not NULL"""
                sql = """
                        SELECT nomepessoa,funcaotecnica,numeroparticipacoescopa
                        FROM
                            (SELECT idpessoa,funcaotecnica,numeroparticipacoescopa FROM
                             membro_selecao NATURAL JOIN selecao WHERE funcaotecnica != 'NULL'
                             AND pais = """ + pais + """ ) AS Comissao NATURAL JOIN pessoa ;
                    """
                result = psql.read_sql(sql,self.conn)

            elif query=='query_jogador_gols':
                posicao, n_gols = args
                # sql = """SELECT * FROM (
                #          SELECT idselecao1,idselecao2 FROM (
                #           SELECT idselecao1,idselecao2
                #           FROM partida NATURAL JOIN selecao AS sel1(idselecao1)
                #          )
                #          AS partida_sel1 NATURAL JOIN selecao AS sel2(idselecao2)
                #         )
                #         AS selecoesDaPartida , (
                #          SELECT funcaotecnica,idselecao,numerogols,posicao FROM membro_selecao
                #          WHERE jogador.funcaotecnica=NULL
                #         )
                #         AS jogador
                #         WHERE selecoesDaPartida.idselecao1 = jogador.idselecao
                #         OR selecoesDaPartida.idselecao2 = jogador.idselecao
                #         AND jogador.numerogols >="""+n_gols+"""
                #         AND jogador.posicao="""+posicao+""";"""

                sql = """SELECT  codpartida, valoringresso , pais1, pais2, partida.nomecidade , partida.datapartida
                 FROM (
                  SELECT DISTINCT datapartida, nomecidade, pais1, pais2 ,idselecao1 ,
                                  idselecao2
                   FROM (
                     SELECT idselecao1 , idselecao2 ,datapartida ,nomecidade,pais1,pais2
                     FROM ( SELECT *
                      FROM partida NATURAL JOIN selecao AS sel1(idselecao1,pais1)
                     )
                      AS partida_sel1 NATURAL JOIN selecao AS sel2(idselecao2,pais2)
                    ) AS todasPartidascomGolsEposicao
                      JOIN ( SELECT idselecao,numerogols,posicao FROM membro_selecao
                             WHERE funcaotecnica = 'NULL' AND numerogols >= """ + n_gols + """ AND
                             posicao=""" + posicao + """
                             ) AS jogador ON (todasPartidascomGolsEposicao.idselecao1 = jogador.idselecao    OR
                                  todasPartidascomGolsEposicao.idselecao2 = jogador.idselecao)
                             )  AS selecoesDaPartida JOIN partida ON
                                 (selecoesDaPartida.idselecao1 = partida.idselecao1 AND
                                  partida.idselecao2 = selecoesDaPartida.idselecao2) ;"""

                result = psql.read_sql(sql,self.conn)

            else:
                # For a pretty table html, make the querry with pandas api, then send result to server
                result = psql.read_sql('SELECT * FROM %s' % query,self.conn)
            # OLD Version of querry without pretty tables
            """self.cursor.execute(command)
            return self.cursor.declare(),self.cursor.fetchall()"""
            return result
    # select()

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
    # update_settings()

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
    # translators()

    def hire_translator(self,idtranslator,condition=None):
        if condition:
            pass
        else:
             # VERIFY IF translator EXISTS
            command = ('SELECT idpessoa FROM tradutor WHERE idpessoa=%s ;' % idtranslator)
            self.cursor.execute(command)
            idtranslator_exists = self.cursor.fetchall()
             # VERIFY IF user has already caontacted a translator
            command = ('SELECT idtorcedor FROM contrata WHERE idtorcedor=%s or idtradutor=%s ;' % (self.id_user,idtranslator))
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
    # hire_translator()

    def contact_guide(self,idguia,condition = None):
        if condition:
            pass
        else:
            # VERIFY IF guide EXISTS
            command = ('SELECT idpessoa FROM guia_voluntario WHERE idpessoa=%s ;' % idguia)
            self.cursor.execute(command)
            idguia_exists = self.cursor.fetchall()
             # VERIFY IF user has already caontacted a guide
            command = ('SELECT idtorcedor FROM ajuda WHERE idtorcedor=%s or idguia=%s;' % (self.id_user,idguia))
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
    # contact_guide()

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
    # guides()

    def matches(self, past=False):
        # Query returns the names of teams that will play in the same match at a data and location
        if past:
            attributes = 'codpartida,selecao1,golselecao1,golselecao2,selecao2,datapartida,nomecidade'
        else:
            attributes = 'codpartida,selecao1,selecao2,datapartida,nomecidade'
        query = 'SELECT %s \
                 FROM \
                ( SELECT * FROM partida NATURAL JOIN selecao AS sel1(idselecao1,selecao1))\
                  AS partida_selecao JOIN selecao AS sel2(idselecao2,selecao2) ON partida_selecao.idselecao2=sel2.idselecao2 ;' % attributes
        result = psql.read_sql(query, self.conn)
        return result
    # matches()

    def increment_goal(self, golselecao, codpartida):
        selecao = 'golselecao' + str(golselecao)
        command = 'UPDATE partida SET %s=%s+1 WHERE codpartida=%s' % (selecao, selecao, codpartida)
        self.cursor.execute(command)
        self.conn.commit()
        result = self.matches(past=True)
        return result
    # increment_goal

    def modify_score(self, gol1, gol2, codpartida):
        command = 'UPDATE partida SET golselecao1=%s, golselecao2=%s WHERE codpartida=%s' % (gol1, gol2, codpartida)
        self.cursor.execute(command)
        self.conn.commit()
        result = self.matches(past=True)
        return result
    # modify_score()

    def buy_tickets(self, codpartida, condition = None):
        if condition:
            pass
        else:
            # VERIFY IF codpartida EXISTS
            command = ('SELECT codpartida FROM partida WHERE codpartida=%s ;' % codpartida)
            self.cursor.execute(command)
            codpartida_exists = self.cursor.fetchall()
             # VERIFY IF user has bought already the same ticket
            command = ('SELECT codpartida FROM compraingresso WHERE codpartida=%s and idpessoa=%s;' % (codpartida,self.id_user))
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
    # buy_tickets()

    def print_results(self,results):
        for item in results:
            print(item)
    # print_results()

    def incrementar_score_jogador (self, id_jogador, score, condition=None):
        '''Incrementa o saldo de gols de um jogador após uma partida'''

        if condition:
            pass
        else:
            # verify that player exists
            command =  ('SELECT numerogols FROM membro_selecao WHERE idpessoa=%s;' % id_jogador)
            self.cursor.execute(command)
            player_exists = self.cursor.fetchall()

            # player exists: update its score
            if player_exists:
                numerogols = player_exists[0][0]
                command = ('UPDATE membro_selecao SET numerogols=%s WHERE idpessoa=%s' % numerogols + score, id_jogador)
                return True
        return False
    # incrementar_score_jogador()

# Connection
