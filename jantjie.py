import sqlite3
import re
import json

GET = {
    r'(?P<id>\d+)':         "SELECT * FROM 'posts' WHERE ID = :id",
    r'^$':                  "SELECT * FROM 'posts'",
    r'say (?P<comment>.*)': "INSERT INTO 'posts' ('comment') VALUES (:comment)",
}

def jantjie(query, conn):
    c = conn.cursor()
    for regex, handler in GET.items():
        m = re.match(regex, query)
        if m:
            c.execute(handler, m.groupdict())
            conn.commit()
            results = c.fetchall()
            if results:
                columns = tuple(dbcol[0] for dbcol in c.description)
                return [{col: val for col, val in zip(columns, result)}
                        for result in results]

def serve(conn):
    cmd = yield
    while True:
        cmd = yield jantjie(cmd, conn)

def http():
    pass


def prompt(routine, ps='? '):
    next(routine)
    cmd = ''
    try:
        while True:
            cmd = input(ps)
            result = routine.send(cmd)
            if result:
                print(result)
    except KeyboardInterrupt:
        return
    except EOFError:
        return


def setup(conn):
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS 'posts' (
            'id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'comment' TEXT,
            'created' TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
    ''')
    conn.commit()

if __name__ == '__main__':
    conn = sqlite3.connect('sqlite.db')
    setup(conn)
    prompt(serve(conn))
