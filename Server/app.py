from flask import Flask
from flask import request
import psycopg2
import urllib.parse as urlparse
import os

DEFAULT_DATABASE = 'database'

database = os.environ.get('DATABASE_URL', DEFAULT_DATABASE)

if database == DEFAULT_DATABASE:
    conn = psycopg2.connect(
            host=database,
            database="td_1",
            user="si5_sacc",
            password="dev_password")
            
else:
    
    url = urlparse.urlparse(database)
    dbname = url.path[1:]
    user = url.username
    password = url.password
    host = url.hostname
    port = url.port


    conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
                )
# create a cursor
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS visits (ip VARCHAR);")
cur.close()
app = Flask(__name__)


@app.route('/')
def hello():
    cur = conn.cursor()
    cur.execute("INSERT INTO visits VALUES('"+str(request.remote_addr)+"')")
    cur.execute('SELECT count(ip)  FROM visits')
    count = str(cur.fetchone())
    count = count[1:count.find(',')]
    cur.close()
    return "Hello, World! The total vist number is now "+ count + "."
