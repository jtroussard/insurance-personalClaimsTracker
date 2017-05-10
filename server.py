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
		login_result = md.login_user(username, password)
		print (login_result)
		if login_result:
			logged = True
			print('login is Something')
			#master = md.get_collection()
			master = []
			return render_template('main.html', master=master)
		else:
			print('login is None')
			return render_template('index.html', logged)

	# default render
	print("\t{}".format(request))
	return render_template('index.html', logged=False)


@app.route('/main', methods=['GET', 'POST'])
def pMain():
	print("===SERVER-MAIN===")
	print("\t{}".format(request))
	print("\t{}".format(request.form))
	if request.method == 'POST':
		if "show-list" in request.form:
			master = md.get_collection()
			return render_template('main.html', master=master)
		elif "hide-list" in request.form:
			master = []
			return render_template('main.html', master=master)
		elif "show-unapproved" in request.form:
			master = md.get_unapproved()
			return render_template('main.html', master=master)
		elif "add-doc" in request.form:
			print("add-doc button pressed")
			print("new item desc: {}".format(request.form['desc']))
			desc  = request.form['desc']
			qty   = request.form['qty']
			owner = request.form['owner']
			room  = request.form['room']
			notes = request.form['notes']

			md.insert_doc(desc, qty, owner, room, notes)			
		

	return render_template('main.html')

# start the server
if __name__ == '__main__':
	app.run('0.0.0.0', port=8080, debug=True)
