# Jacques J. Troussard
# Insurance Tracker Project
#
# DB Methods

import pymongo
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











