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

	login_result = collection.find_one({ 'username': rqst_user, 'password': rqst_password })
	print("\tlogin results: {}".format(login_result))
	return (login_result)







