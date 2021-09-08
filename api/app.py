from enum import unique
from os import name
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost:3308/servihogar'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(25), nullable=False)
    birthDate = db.Column(db.DateTime(), nullable=False)
    address = db.Column(db.String(40), nullable=False)
    locality_id = db.Column(db.Integer, nullable=False)
    locality = db.relationship('Locality', backref='user', lazy=False, primaryjoin="Locality.id == foreign(User.locality_id)")

    def __init__(self, name, email, username, password, birthdate, address, locality):
        self.name = name
        self.email = email
        self.username = username
        self.password = password
        self.birthdate = birthdate
        self.address = address
        self.locality = locality

class Locality(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    city = db.Column(db.String(40), nullable=False)
    postalCode = db.Column(db.Integer, nullable=False)
    province_id = db.Column(db.Integer, nullable=False)
    province = db.relationship('Province', backref='locality', lazy=False, primaryjoin="Province.id == foreign(Locality.province_id)")

    def __init__(self, city, postalCode, province):
        self.city = city
        self.postalCode = postalCode
        self.province = province

class Province(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(40), nullable=False)

    def __init__(self, name):
        self.name = name

db.create_all()

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'username', 'password', 'birthdate', 'address', 'locality')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class LocalitySchema(ma.Schema):

    class Meta:
        fields = ('id', 'city', 'postalCode', 'province')

locality_schema = LocalitySchema()
localities_schema = LocalitySchema(many=True)

class ProvinceSchema(ma.Schema):

    class Meta:
        fields = ('id', 'name')

province_schema = ProvinceSchema()
provinces_schema = ProvinceSchema(many=True)

@app.route('/users', methods=['POST'])
def create_user():

    name = request.json['name']
    email = request.json['email']
    username = request.json['username']
    password = request.json['password']
    birthdate = request.json['birthdate']
    address = request.json['address']
    locality = request.json['locality']

    new_user = User(name, email, username, password, birthdate, address, locality)
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

@app.route('/users', methods=['GET'])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return user_schema.jsonify(result)

@app.route('/users/<id>')
def get_user(id):
    user = User.query.get(id)
    return jsonify(user)

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)

    name = request.json['name']
    email = request.json['email']
    username = request.json['username']
    password = request.json['password']
    birthdate = request.json['birthdate']
    address = request.json['address']
    locality = request.json['locality']

    user.name = name
    user.email = email
    user.username = username
    user.password = password
    user.birthdate = birthdate
    user.address = address
    user.locality = locality

    db.session.commit()

    return user_schema.jsonify(user)

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)

    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)

@app.route('/localities', methods=['POST'])
def create_locality():

    city = request.json['city']
    postalCode = request.json['postalCode']
    province = request.json['province']

    new_locality = Locality(city, postalCode, province)
    db.session.add(new_locality)
    db.session.commit()

    return locality_schema.jsonify(new_locality)

@app.route('/provinces', methods=['POST'])
def create_province():

    name = request.json['name']

    new_province = Province(name)
    db.session.add(new_province)
    db.session.commit()

    return locality_schema.jsonify(new_province)

@app.route('/')
def index():
    return jsonify({"message": "What are you expecting to find here?"})

if __name__ == "__main__":
    app.run(debug=True)