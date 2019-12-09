from flask import Flask 
from flask_sqlalchemy import SQLAlchemy #may need pip install!?
#import sqlalchemy.dialects.sqlite
import json
from settings import app #import app Object specifically 

#creating a database Object
db = SQLAlchemy(app)  #calling SQLAlchemy Constructor and passing it the app Object

#class Book inherit from db.Model
class Book(db.Model):
	#define tablename 
	__tablename__ = 'books'
	#define columns 
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False) #cant be NULL
	price = db.Column(db.Float, nullable=False)
	isbn = db.Column(db.Integer)

	# __repr__ method is useful only in Terminal
	#so we define a new method for json output
	def json(self):
		return{'name': self.name, 'price':self.price, 'isbn': self.isbn}

	#Adding books 
	def add_book(_name, _price, _isbn):
		new_book=Book(name=_name, price=_price, isbn=_isbn)
		db.session.add(new_book)
		db.session.commit()  #to save the changes

	#get all books	
	def get_all_books():
		return [Book.json(book) for book in Book.query.all()]

	#get book by isbn	
	def get_book(_isbn):
		return Book.json(Book.query.filter_by(isbn=_isbn).first())

	#delete book by isbn	
	def delete_book(_isbn):
		is_successful = Book.query.filter_by(isbn=_isbn).delete()
		db.session.commit() #To save the changes
		return bool(is_successful)	

	#to update a property (using Dot notation)	
	def update_book_name(_isbn, _name):
		book_to_update = Book.query.filter_by(isbn=_isbn).first()
		book_to_update.name = _name #using Dot notation,update property 'name'
		db.session.commit() #save changes

	def update_book_price(_isbn, _price):
		book_to_update = Book.query.filter_by(isbn=_isbn).first()
		book_to_update.price = _price
		db.session.commit()	#save changes

	#to replace Table Entries
	def replace_book(_isbn, _name, _price):
		book_to_replace = Book.query.filter_by(isbn=_isbn).first()
		book_to_replace.name = _name
		book_to_replace.price = _price
		db.session.commit()	

	#output representation	
	def __repr__(self):
		book_object={
			'name': self.name,
			'price': self.price,
			'isbn': self.isbn
		}
		return json.dumps(book_object)