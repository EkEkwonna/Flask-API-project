"""
REST - Representational State Transfer
HTTP Service - that can be accessed through a browser that can be called 
using standard commands (we can go to a browser and contact it and 
simply request information)


API - Application Programming Interface
A simple contract / interface between the application offering it and 
a third party application. 

We request information through HTTP - endpoints

GET - retrieve data 
POST - add new data
PUT/PATCH - updated data 
DELETE - remove data 
"""

# Start by activating virtual environment (conda activate .flask_env)
# To create a requirements.txt file to see the package dependencies of the venv
# From the virtual Environment run the following: pip freeze > requirements.txt

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource,Api,reqparse,fields, marshal_with , abort 

app = Flask(__name__)

#Configuring a Database that we will name database db under SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique = True, nullable = False)
    email = db.Column(db.String(80), unique = True, nullable = False)

    def __repr__(self): 
        return f"User (name = {self.name}, email = {self.email})"
    

user_args = reqparse.RequestParser()
user_args.add_argument('name',type = str,required = True , help = 'Name cannot be blank')
user_args.add_argument('email',type = str,required = True , help = 'Email cannot be blank')

@app.route('/')
def home():
    return '<h1>Flask REST API<h1>'

if __name__ == '__main__':

    #Good to do this in development but not in Production
    app.run(debug = True) 























