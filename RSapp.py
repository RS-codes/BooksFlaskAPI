from flask import Flask, jsonify,request,Response

from BookModel import *
from settings import *

import json   			 #import Json
from settings import *   #import all

import jwt, datetime  #import jwt library which has JWT encode method
from UserModel import User  #import User
from functools import wraps #for method token_required

app.config['SECRET_KEY'] = 'meow'

@app.route('/login',methods=['POST'])
def get_token():
	request_data = request.get_json()
	username = str(request_data['username'])
	password = str(request_data['password'])

	match = User.username_password_match(username, password)

	if match:
		expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
		token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'],algorithm='HS256')
		return token
	else:
		return Response('', 401, mimetype='application/json')


#request body
#{
#	'name' : 'Newbook',
#	'price' : 456,
#	'isbn' : 369852
#}

 #Sanitize the data received from Client
#if "keyName" in dictionaryObject
def validBookObject(bookObject):
	if ("name" in bookObject 
		and "price" in bookObject 
			and "isbn" in bookObject):
		return True
	else:
		return False	

#Adding a POST route
#POST/books
@app.route('/books', methods=['POST'])
def add_book():
	request_data = request.get_json()#get the req.data by get_json method 
	if(validBookObject(request_data)): #considering only validObject is sent
		Book.add_book(request_data['name'], request_data['price'], request_data['isbn'])
		response = Response("", status=201, mimetype='application/json')
		response.headers['Location'] = "/books" + str(request_data['isbn'])
		return response
	else:
		invalidBookObjectErrorMsg = {
			"error" : "Invalid book object in request",
			"helpString" : "Pls pass Data in similar format {'name':'bookname', 'price':5.9, 'isbn':852569}" 
		}
		response = Response(json.dumps(invalidBookObjectErrorMsg),status=400,mimetype='application/json')
		return response


#wrapper method replaces the function being decorated
def token_required(f):
	@wraps(f)
	def wrapper(*args, **kwargs): #wrapper method takes arguments and keywords
		token = request.args.get('token')
		try:
			jwt.decode(token, app.config['SECRET_KEY'])
			return f(*args, **kwargs)
		except:
			return jsonify({'error': 'Need a valid token'}),401
	return wrapper		

#GET/books?token=asok9f09rtwi978hs
@app.route('/books')
@token_required
def get_all_books():
	return jsonify({'Books':Book.get_all_books()}) #from database

#GET/books/isbn
@app.route('/books/<int:isbn>')
def get_by_isbn(isbn):
	return_value=Book.get_by_isbn(isbn)
	return jsonify(return_value)

#PUT /books/5869
#{
# 'name': 'NewName',
# 'price': 456	
#}
"""
to update a single field ,we use PATCH request(will discuss later)
"""

def valid_put_request_data(request_data):
	if ("name" in request_data 
		and "price" in request_data):
		return True
	else:
		return False

#PUT route
@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
	request_data=request.get_json()
	if(not valid_put_request_data(request_data)):
		invalidBookObjectErrorMsg = {
			"error" : "Invalid book object in request",
			"helpString" : "Pls pass Data in similar format {'name':'bookname', 'price':5.9, 'isbn':852569}" 
		}
		response = Response(json.dumps(invalidBookObjectErrorMsg),status=400,mimetype='application/json')
		return response

	Book.replace_book(isbn, request_data['name'],request_data['price'])	
	response = Response("", status=204) #No content created
	return response

# PATCH /books/isbn
#{
#	'name': 'UpdateNameAlone'
#}

# PATCH /books/isbn
#{
#	'price': 'UpdatePriceAlone'	
#}


def valid_patch_request_data(request_data):
	if ("name" in request_data 
		or "price" in request_data):
		return True
	else:
		return False

@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
	request_data = request.get_json() #we get the JSON data
	if(not valid_patch_request_data(request_data)):
		invalidBookObjectErrorMsg = {
			"error": "Invalid book object passed in request",
			"helpstring": "Data should be in following format{'name': 'bookname', 'price':15}"
		}
		response = Response (json.dumps(invalidBookObjectErrorMsg),staus=404,mimetype='application/json')
		return response
	
	if("name" in request_data):
		Book.update_book_name(isbn, request_data['name'])
	if("price" in request_data):
		Book.update_book_price(isbn, request_data['price'])
	
	response = Response("",status=204) #204=Success
	response.headers['Location'] = "/books/" + str(isbn)
	return response

#DELETE /books/isbn
@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
	if(Book.delete_book(isbn)):
		response = Response("",status=204)
		return response

	invalidBookObjectErrorMsg = {
		"error":"Unable to Delete,as ISBN provided doesnot found in the List"
	}
	response = Response(json.dumps(invalidBookObjectErrorMsg),status=404, mimetype='application/json') #Status404:Resource not found	
	return response

app.run(port=5000)