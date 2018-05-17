import psycopg2

def main():
    conn = psycopg2.connect('dbname=mydb user=andrewjschuang')
    cur = conn.cursor()

    printResults(select(cur, 'cities'))

    cur.close()
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

if __name__ == '__main__':
    main()
