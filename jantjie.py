import sqlite3
import re
import json
import http.server
import urllib.parse as urlparse

GET = {
    r'/(?P<id>\d+)$':       "SELECT * FROM 'posts' WHERE ID = :id",
    r'/$':                  "SELECT * FROM 'posts'",
    r'/say (?P<comment>.*)': "INSERT INTO 'posts' ('comment') VALUES (:comment)",
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


def jantjie_handler(conn):
    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            path = urlparse.urlparse(self.path).path
            query = dict(urlparse.parse_qsl(urlparse.urlparse(self.path).query))
            print(path, query)
            result = jantjie(path, conn)
            self.wfile.write(json.dumps(result).encode())
            return
    return Handler



def serve(conn):
    cmd = yield
    while True:
        cmd = yield jantjie(cmd, conn)

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
    httpd = http.server.HTTPServer(('', 8000), jantjie_handler(conn))
    httpd.serve_forever()
