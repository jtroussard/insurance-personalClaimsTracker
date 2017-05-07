import os
import psycopg2
import psycopg2.extras
import uuid
import datetime
import time

from lib.config import *
from lib import data_mongo as md
from flask import Flask, render_template, request, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

logged = True

@app.route('/', methods=['GET', 'POST'])
def pIndex():
	print("===SERVER-INDEX===")

	# login attempt
	if request.method == 'POST':
		print("\t{}".format(request))
		print("\t{}".format(request.form))
		username = request.form['user']
		password = request.form['password']
		print ("\t{}  {}".format(username, password))
#		login_result = md.loginUser(checkLogin()
		return render_template('main.html')

	# default render
	print("\t{}".format(request))
	return render_template('index.html')


@app.route('/main', methods=['GET', 'POST'])
def pMain():
	print("===SERVER-MAIN===")
	return render_template('main.html')

# start the server
if __name__ == '__main__':
	app.run('0.0.0.0', port=8080, debug=True)
