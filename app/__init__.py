from flask import Flask
from flask.ext.mysql import MySQL

app = Flask(__name__)
app.debug = True

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '111222'
app.config['MYSQL_DATABASE_DB'] = 'tp_db'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)

conn = mysql.connect()
conn.autocommit(True)
cursor = conn.cursor()

from app import User, Forum, Thread, Post,generic
