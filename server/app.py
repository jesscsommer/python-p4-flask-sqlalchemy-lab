#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.filter(Animal.id == id).first()

    if not animal: 
        response_body = "<h1>404 animal not found</h1>"
        response = make_response(response_body, 404)
        return response
    
    name = f"<ul>Name: {animal.name}</ul>"
    species = f"<ul>Species: {animal.species}</ul>"
    zookeeper = f"<ul>Zookeeper: {animal.zookeeper.name}</ul>"
    enclosure = f"<ul>Enclosure: {animal.enclosure.id}</ul>"

    response_body = "".join([name, species, zookeeper, enclosure])
    response = make_response(response_body, 200)
    return response

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.filter(Zookeeper.id == id).first()

    if not zookeeper: 
        response_body = "<h1>404 zookeeper not found</h1>"
        response = make_response(response_body, 404)
        return response
    
    name = f"<ul>Name: {zookeeper.name}</ul>"
    birthday = f"<ul>Birthday: {zookeeper.birthday}</ul>"
    animals = ""
    
    for animal in zookeeper.animals: 
        new_animal = f"<ul>{animal}</ul>"
        animals = "".join([animals, new_animal])

    response_body = "".join([name, birthday, animals])
    response = make_response(response_body, 200)
    return response

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.filter(Enclosure.id == id).first()

    if not enclosure: 
        response_body = "<h1>404 enclosure not found</h1>"
        response = make_response(response_body, 404)
        return response
    
    environment = f"<ul>Environment: {enclosure.environment}</ul>"
    open_to_visitors = f"<ul>Open to Visitors: {enclosure.open_to_visitors}</ul>"
    animals = ""
    
    for animal in enclosure.animals: 
        new_animal = f"<ul>{animal}</ul>"
        animals = "".join([animals, new_animal])

    response_body = "".join([environment, open_to_visitors, animals])
    response = make_response(response_body, 200)
    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
