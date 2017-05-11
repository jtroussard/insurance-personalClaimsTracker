# Jacques J. Troussard
# Insurance Tracker Project
#
# DB Methods

import pymongo
import datetime
from lib.config import *
from pymongo import MongoClient

def ConnectToMongo():
	try:
		client = MongoClient()
		return(client)
	except Exception as e:
		print(type(e))
		print(e)
		print ("Error connecting with MongoClient")
		return None

def get_db(client, database):
	try:
		db = db = client.database
		return (db)
	except Exception as e:
		print(type(e))
		print(e)
		print ("Error getting database")
		return None

def get_collection():
	print("===MONGO-GETCOLLECTION===")
	try:
		conn = ConnectToMongo();
		db = conn.insurance
		collection = db.master
		results = collection.find()
		print("\tresult test:{}".format(results))
		return (results)
	except Exception as e:
		print(type(e))
		print(e)
		print ("Error getting collection")

		
def login_user(rqst_user, rqst_password):
	print("===MONGO-LOGIN===")
	print("\targs= {}, {}".format(rqst_user, rqst_password))
	conn = ConnectToMongo();
	if conn == None:
		print ('Connection Error: Login Aborted')
		return None
	
	db = conn.insurance
	collection = db.users

	login_result = collection.find_one({ 'username': rqst_user, 'password':
			rqst_password })
	print("\tlogin results: {}".format(login_result))
	return (login_result)


def insert_doc(rq_description, rq_qty, rq_owner, rq_room, rq_notes):
	print("===MONGO-INSERTDOC===")
	print("\targs= {}, {}, {}, {}, {}".format(rq_description, rq_qty, rq_owner,
				rq_room, rq_notes))
	conn = ConnectToMongo();
	if conn == None:
		print("Connection Error: Insert Doc Aborted")
		return None
	
	db = conn.insurance
	collection = db.master
	original_count = collection.count()
	sequence = collection.count() + 1

	collection.insert_one(
		{
			"seq" : sequence,
			"orig-desc" : rq_description,
			"qty" : rq_qty,
			"owner" : rq_owner,
			"room" : rq_room,
			"original" : "FALSE",
			"modified" : "FALSE",
			"replaced" : "FALSE",
			"reimbursed" : "FALSE",
			"notes" : rq_notes,
			"approved" : "FALSE"
		}
	)
	print(collection.find({"seq":389}))
	if (original_count < collection.count()):
		print("\tDoc insert SUCCESSFUL")
	else:
		print("\tDoc insert UNSUCCESSFUL")


def get_unapproved():
	print("===MONGO-GETUNAPPROVED===")
	try:
		conn = ConnectToMongo();
		db = conn.insurance
		collection = db.master
		results = collection.find({"approved" : "FALSE"})
		print("\tresult test:{}".format(results))
		return (results)
	except Exception as e:
		print(type(e))
		print(e)
		print ("Error getting unapproved collection")


def rtn_doc(r_seq):
	print("===MONGO-GETACTIVEDOC===")
	print("\targs= {}".format(r_seq))

	conn = ConnectToMongo();
	if conn == None:
		print("Connection Error: Insert Doc Aborted")
		return None

	db = conn.insurance
	collection = db.master
	active_doc = collection.find_one( { 'seq' : int(r_seq) } ) 
	print(active_doc)

	if not active_doc:
		print("Sequence number is not in database")
	
	return active_doc


#history is a list of objects


def mod_doc(r_seq, r_repl_desc, r_orig_desc, r_qty, r_unit_price, r_est_amt, r_tax,
		r_repl_cost, r_depr, r_acv, r_owner, r_room, r_original, r_modified,
		r_replaced, r_reimbursed, r_invoice, r_notes):
	
	print("===MONGO-MODDOC===")
	print("\targs= {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(r_repl_desc, r_orig_desc, r_qty, r_unit_price, r_est_amt, r_tax, r_repl_cost, r_depr, r_acv, r_owner, r_original, r_modified,	r_replaced, r_reimbursed, r_invoice, r_notes, r_room))
	conn = ConnectToMongo();
	if conn == None:
		print("Connection Error: Insert Doc Aborted")
		return None

	db = conn.insurance
	collection = db.master
	original_doc = collection.find_one( {"seq": int(r_seq) } )
	history_entry = {}
	record_entry = ""

	for key in original_doc:
		print(key)
	
	if 'repl-desc' in original_doc and r_repl_desc != original_doc['repl-desc']:
		record_entry += "replacement desc: " + original_doc['repl-desc'] + " => " + r_repl_desc + "\n"
	else:
		original_doc = { 'repl-desc' : r_repl_desc }
		record_entry += "replacement desc: EMPTY => " + r_repl_desc + "\n"

	if 'orig-desc' in original_doc and r_orig_desc != original_doc['orig-desc']:
		record_entry += "original desc: " + original_doc['orig-desc'] + " => " + r_orig_desc + "\n"
	else:
		original_doc = { 'orig-desc' : r_orig_desc }
		record_entry += "original desc: EMPTY => " + r_orig_desc + "\n"

	if 'qty' in original_doc and r_qty != original_doc['qty']:
		record_entry += "qty: " + original_doc['qty'] + " => " + r_qty + "\n"
	else:
		original_doc = { 'qty' : r_qty }
		record_entry += "qty: EMPTY => " + r_qty + "\n"

	if 'unit-price' in original_doc and r_unit_price != original_doc['unit-price']:
		record_entry += "unit price: " + original_doc['unit-price'] + " => " + r_unit_price + "\n"
	else:
		original_doc = { 'unit-price' : r_unit_price }
		record_entry += "unit price: EMPTY => " + r_unit_price + "\n"

	if 'est-amt' in original_doc and r_est_amt != original_doc['est-amt']:
		record_entry += "estimate amount: " + original_doc['est-amt'] + " => " + r_est_amt + "\n"
	else:
		original_doc = { 'est-amt' : r_est_amt }
		record_entry += "estimate amount: EMPTY => " + r_est_amt + "\n"
	
	if 'tax' in original_doc and r_tax != original_doc['tax']:
		record_entry += "additional: " + original_doc['tax'] + " => " + r_tax + "\n"
	else:
		original_doc = { 'tax' : r_tax }
		record_entry += "additional: EMPTY => " + r_tax + "\n"

	if 'repl-cost' in original_doc and r_repl_cost != original_doc['repl-cost']:
		record_entry += "replacement cost: " + original_doc['repl-cost'] + " => " + r_repl_cost + "\n"
	else:
		original_doc = { 'repl-cost' : r_repl_cost }
		record_entry += "replacement cost: EMPTY => " + r_repl_cost + "\n"
	
	if 'depr' in original_doc and r_depr != original_doc['depr']:
		record_entry += "depreciation: " + original_doc['depr'] + " => " + r_depr + "\n"
	else:
		original_doc = { 'depr' : r_depr }
		record_entry += "depreciation: EMPTY => " + r_depr + "\n"

	if 'acv' in original_doc and r_acv != original_doc['acv']:
		record_entry += "actual value" + original_doc['actual value'] + " => " + r_acv + "\n"
	else:
		original_doc = { 'acv' : r_acv }
		record_entry += "actual value: EMPTY  => " + r_acv + "\n"

	if 'replaced' in original_doc and r_replaced != original_doc['replaced']:
		record_entry += "replaced: " + original_doc['replaced'] + " => " + r_replaced + "\n"
	else:
		original_doc = { 'replaced' : r_replaced }
		record_entry += "replaced: EMPTY => " + r_replaced + "\n"

	if 'reimbursed' in original_doc and r_reimbursed != original_doc['reimbursed']:
		record_entry += "reimbursed: " + original_doc['reimbursed'] + " => " + r_reimbursed + "\n"
	else:
		original_doc = { 'reimbursed' : r_reimbursed }
		record_entry += "reimbursed: EMPTY => " + r_reimbursed + "\n"

	if 'invoice' in original_doc and r_invoice != original_doc['invoice']:
		record_entry += "invoice: " + original_doc['invoice'] + " => " + r_invoice + "\n"
	else:
		original_doc = { 'invoice' : r_invoice }
		record_entry += "invoice: EMPTY => " + r_invoice + "\n"

	if 'notes' in original_doc and r_notes != original_doc['notes']:
		record_entry += "notes: " + original_doc['notes'] + " => " + r_notes + "\n"
	elif :
		original_doc = { 'notes' : r_notes }
		record_entry += "notes: EMPTY => " + r_notes + "\n"

	now = datetime.datetime.now()
	history_entry = { "date" : now, "record" : record_entry, }

	collection.find_one_and_update(	{"seq"  :int(r_seq)},
									{"$set" : {
										"repl-desc" : r_repl_desc,
										"orig-desc" : r_orig_desc,
										"qty"       : r_qty,
										"unit-price": r_unit_price,
										"est-amt"   : r_est_amt,
										"tax"       : r_tax,
										"repl-cost" : r_repl_cost,
										"depr"      : r_depr,
										"acv"       : r_acv,
										"owner"     : r_owner,
										"room"      : r_room,
										"original"  : r_original,
										"modified"  : r_modified,
										"replaced"  : r_replaced,
										"reimbursed": r_reimbursed,
										"invoice"   : r_invoice,
										"notes"     : r_notes
										},
									"$addToSet" : { "history" : history_entry }
									})
	print(collection.find_one( { "seq" : int(r_seq) } ))





