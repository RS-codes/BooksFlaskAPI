from flask_sqlalchemy import SQLAlchemy 
from settings import app

db = SQLAlchemy(app)

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	password = db.Column(db.String(80), nullable=False)

	#printable representation of a given object
	def __repr__(self):
		return str({
			'username': self.username,
			'password': self.password
		})

	#username/password match ftn,
	#acts as API to determine whether someone should get access
	def username_password_match(_username, _password):
		user = User.query.filter_by(username=_username).filter_by(password=_password).first()
		if user is None:
			return False
		else:
			return True

	
	#getAllUsers method
	def getAllUsers():
		return User.query.all() #returns in the representation format given at top

	#createUser method
	def createUser(_username, _password):
		new_user = User(username=_username, password=_password)
		db.session.add(new_user)
		db.session.commit() 	
