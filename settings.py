from flask import Flask 


#Flask Constructor to create app Object
app = Flask(__name__) #this app Object is shared with RSapp.py file

#config to store SQLALCHEMY_DATABASE_URI,
#this will be the path where we'll store database

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/rs/RSflaskAPI/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
