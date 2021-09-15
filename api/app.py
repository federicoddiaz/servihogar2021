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
    birthdate = db.Column(db.DateTime(), nullable=False)
    address = db.Column(db.String(40), nullable=False)
    city_id = db.Column(db.Integer, nullable=False)
    city = db.relationship('City', backref='user', lazy=False, primaryjoin="City.id == foreign(User.city_id)")

    def __init__(self, name, email, username, password, birthdate, address, city_id):
        self.name = name
        self.email = email
        self.username = username
        self.password = password
        self.birthdate = birthdate
        self.address = address
        self.city_id = city_id

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(40), nullable=False)
    postalCode = db.Column(db.String(40), nullable=False)
    province_id = db.Column(db.Integer, nullable=False)
    province = db.relationship('Province', backref='city', lazy=False, primaryjoin="Province.id == foreign(City.province_id)")

    def __init__(self, name, postalCode, province_id):
        self.name = name
        self.postalCode = postalCode
        self.province_id = province_id

class Province(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(40), nullable=False)

    def __init__(self, name):
        self.name = name

db.create_all()

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'username', 'password', 'birthdate', 'address', 'city_id')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class CitySchema(ma.Schema):

    class Meta:
        fields = ('id', 'name', 'postalCode', 'province_id')

city_schema = CitySchema()
cities_schema = CitySchema(many=True)

class ProvinceSchema(ma.Schema):

    class Meta:
        fields = ('id', 'name')

province_schema = ProvinceSchema()
provinces_schema = ProvinceSchema(many=True)

#--------------USER--------------

@app.route('/users', methods=['POST'])
def create_user():

    name = request.json['name']
    email = request.json['email']
    username = request.json['username']
    password = request.json['password']
    birthdate = request.json['birthdate']
    address = request.json['address']
    city_id = request.json['city_id']

    new_user = User(name, email, username, password, birthdate, address, city_id)
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

@app.route('/users', methods=['GET'])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return users_schema.jsonify(result)

@app.route('/users/<id>')
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)

    name = request.json['name']
    email = request.json['email']
    username = request.json['username']
    password = request.json['password']
    birthdate = request.json['birthdate']
    address = request.json['address']
    city_id = request.json['city_id']

    user.name = name
    user.email = email
    user.username = username
    user.password = password
    user.birthdate = birthdate
    user.address = address
    user.city_id = city_id

    db.session.commit()

    return user_schema.jsonify(user)

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)

    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)

#--------------CITY--------------

@app.route('/cities', methods=['POST'])
def create_city():

    name = request.json['name']
    postalCode = request.json['postalCode']
    province_id = request.json['province_id']

    new_city = City(name, postalCode, province_id)
    db.session.add(new_city)
    db.session.commit()

    return city_schema.jsonify(new_city)

@app.route('/cities', methods=['GET'])
def get_cities():
    all_cities = City.query.all()
    result = cities_schema.dump(all_cities)
    return cities_schema.jsonify(result)

@app.route('/cities/<id>')
def get_city(id):
    city = City.query.get(id)
    return city_schema.jsonify(city)

@app.route('/cities/<id>', methods=['PUT'])
def update_city(id):
    city = City.query.get(id)

    name = request.json['name']
    postalCode = request.json['postalCode']
    province_id = request.json['province_id']

    city.name = name
    city.postalCode = postalCode
    city.province_id = province_id

    db.session.commit()

    return city_schema.jsonify(city)

@app.route('/cities/<id>', methods=['DELETE'])
def delete_city(id):
    city = City.query.get(id)

    db.session.delete(city)
    db.session.commit()

    return city_schema.jsonify(city)

#--------------PROVINCE--------------

@app.route('/provinces', methods=['POST'])
def create_province():

    name = request.json['name']

    new_province = Province(name)
    db.session.add(new_province)
    db.session.commit()

    return province_schema.jsonify(new_province)

@app.route('/provinces', methods=['GET'])
def get_provinces():
    all_provinces = Province.query.all()
    result = provinces_schema.dump(all_provinces)
    return provinces_schema.jsonify(result)

@app.route('/provinces/<id>')
def get_province(id):
    province = Province.query.get(id)
    return province_schema.jsonify(province)

@app.route('/provinces/<id>', methods=['PUT'])
def update_province(id):
    province = Province.query.get(id)

    name = request.json['name']

    province.name = name

    db.session.commit()

    return province_schema.jsonify(province)

@app.route('/provinces/<id>', methods=['DELETE'])
def delete_province(id):
    province = Province.query.get(id)

    db.session.delete(province)
    db.session.commit()

    return province_schema.jsonify(province)

@app.route('/')
def index():
    return jsonify({"message": "Welcome to ServiHogar"})

if __name__ == "__main__":
    app.run(debug=True)