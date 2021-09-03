from enum import unique
from os import name
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost:3308/servihogar'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

db.create_all()

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route('/users', methods=['POST'])
def create_user():

    name = request.json['name']
    email = request.json['email']

    new_user = User(name, email)
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

if __name__ == "__main__":
    app.run(debug=True)