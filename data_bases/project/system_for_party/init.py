import psycopg2
import api


def start():
    try:
        conn = psycopg2.connect(
            dbname='student', user='init', password='qwerty', host='localhost')
    except:
        print('Error establishing connection to DB')
        return None, None
    cur = conn.cursor()
    cur.execute(open('domains.sql', 'r').read())
    cur.execute(open('create_tables.sql', 'r').read())
    cur.execute(open('triggers.sql', 'r').read())
    cur.execute(open('user.sql', 'r').read())
    conn.commit()
    cur.close()
    conn.close()
