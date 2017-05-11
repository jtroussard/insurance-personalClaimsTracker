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
	master = []
	active_doc = []
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
		elif "rtn-doc" in request.form:
			active_doc_num = request.form['active_doc_seq']
			active_doc = md.rtn_doc(request.form['active_doc_seq'])
			return render_template('main.html', master=master, active_doc=active_doc)
		elif "mod-doc" in request.form:
			print("\t\t---mod-doc---")
			seq = request.form['m_seq']
			rds = request.form['m_repl-desc']
			ods = request.form['m_orig-desc']
			qty = request.form['m_qty']
			upr = request.form['m_unit-price']
			est = request.form['m_est-amt']
			add = request.form['m_tax']
			rpl = request.form['m_repl-cost']
			dep = request.form['m_depr']
			acv = request.form['m_acv']
			own = request.form['m_owner']
			rom = request.form['m_room']
			org = request.form['m_original']
			mod = request.form['m_modified']
			rmb = request.form['m_reimbursed']
			print(request.form['m_replaced'])			
			rpp = request.form['m_replaced']
			print("CHECKING, acv, est, add, rpl, dep, rmb")
			inv = request.form['m_invoice']
			nts = request.form['m_notes']
			md.mod_doc(seq, rds, ods, qty, upr, est, add, rpl, dep, acv, own, rom, org, mod, rpp, rmb, inv, nts)
			return render_template('main.html', master=master, active_doc=active_doc)	
		elif "add-doc" in request.form:
			print("add-doc button pressed")
			print("new item desc: {}".format(request.form['desc']))
			desc  = request.form['desc']
			qty   = request.form['qty']
			owner = request.form['owner']
			room  = request.form['room']
			notes = request.form['notes']

			md.insert_doc(desc, qty, owner, room, notes)			
		

	return render_template('main.html', master=master, active_doc=active_doc)

# start the server
if __name__ == '__main__':
	app.run('0.0.0.0', port=8080, debug=True)
