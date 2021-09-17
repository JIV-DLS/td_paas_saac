from flask import Flask
from flask import request
from flask import jsonify
import psycopg2
import os

database = os.environ.get('DATABASE_URL', 'database')

print(os.environ['DATABASE_URL'] if 'DATABASE_URL' in os.environ['DATABASE_URL'] else 'database')
conn = psycopg2.connect(
    host=database,
    database="td_1",
    user="si5_sacc",
    password="dev_password")

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
