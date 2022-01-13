from flask import Flask
from flask_mysqldb import MySQL


host, port = "0.0.0.0", 5000
app = Flask(__name__)
app.config.from_pyfile('config.py')

db = MySQL(app)

from views import *

if __name__ == '__main__':
    app.run(debug=True, host=host, port=port)