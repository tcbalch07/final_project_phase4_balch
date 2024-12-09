import pymysql
from flask import g

def get_db():
    if 'db' not in g or not is_connection_open(g.db):
        g.db = pymysql.connect(
            host='wvulqmhjj9tbtc1w.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',
            user='u7rzxd64w9e61z52',
            password='gfwdfas8t3jw4e6y',
            database='os87hp14p6f36rkh',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db

def is_connection_open(conn):
    try:
        conn.ping(reconnect=True)
        return True
    except:
        return False

def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None and not db._closed:
        db.close()