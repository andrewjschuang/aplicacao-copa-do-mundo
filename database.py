import psycopg2

def init(dbname='mydb', user='andrewjschuang'):
    conn = psycopg2.connect(dbname=dbname, user=user)
    cursor = conn.cursor()

    # result = select(cursor, 'cities')
    # printResults(result)

    return (conn, cursor)

def close(conn, cursor):
    cursor.close()
    conn.close()

def select(cursor, relation, condition=None):
    if condition:
        pass
    else:
        command = ('SELECT * FROM %s' % relation)
    cursor.execute(command)
    return cursor.fetchall()

def printResults(results):
    for item in results:
        print(item)
