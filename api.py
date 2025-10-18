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
    displayname= db.Column(db.String(80), nullable = False)
    email = db.Column(db.String(80), unique = True, nullable = False)

    def __repr__(self): 
        return f"User (username = {self.username}, full name = {self.displayname} , email = {self.email})"
    

#Used to validate the data with certain constraits 
user_args = reqparse.RequestParser()
user_args.add_argument('displayname',type = str,required = True , help = 'Full Name cannot be blank')
user_args.add_argument('username',type = str,required = True , help = 'Name cannot be blank')
user_args.add_argument('email',type = str,required = True , help = 'Email cannot be blank')

userFields = {
    'id':fields.Integer, 
    'displayname':fields.String,
    'username':fields.String,
    'email':fields.String

}

class Users(Resource):

    #Marshal_with allows us to serialise the data : allows us to send a json in serialised format

    @marshal_with(userFields)
    def get(self):
        users = UserModel.query.all()
        return users
    
    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(displayname = args['displayname'], username = args['username'], email = args['email'])
        db.session.add(user)
        db.session.commit()
        users = UserModel.query.all()
        return user , 201


class User(Resource):
    @marshal_with(userFields)
    def get(self,id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404,'User not found')
        return user
    
    @marshal_with(userFields)
    def patch(self,id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404,'User not found')
        user.displayname = args['displayname']
        user.username= args['username']
        user.email = args['email']
        db.session.commit()
        return user
    
    @marshal_with(userFields)
    def delete(self,id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404,'User not found')
        db.session.delete(user)
        db.session.commit()
        users = UserModel.query.all()
        return users , 200
        
    


api.add_resource(Users, '/api/users/')
api.add_resource(User, '/api/users/<int:id>/')

@app.route('/')
def home():
    return '<h1>Flask REST API<h1>'

if __name__ == '__main__':

    #Good to do this in development but not in Production
    app.run(debug = True) 























