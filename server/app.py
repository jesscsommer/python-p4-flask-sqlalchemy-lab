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
    # animal = Animal.query.get(id)
    # animal = Animal.query.filter_by(id=id).first_or_404()
    if animal := db.session.get(Animal, id):
        response_body = f"""
            <ul>ID: {animal.id}</ul>
            <ul>Name: {animal.name}</ul>
            <ul>Species: {animal.species}</ul>
            <ul>Zookeeper: {animal.zookeeper.name}</ul>
            <ul>Enclosure: {animal.enclosure.environment}</ul>
        """
        status_code = 200
    else: 
        response_body = f"""
            <ul>404 Not Found: No animal with id {id} </ul>
        """
        status_code = 404

    return make_response(response_body, status_code)

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    if zookeeper := db.session.get(Zookeeper, id):
        response_body = f"""
            <ul>ID: {zookeeper.id}</ul>
            <ul>Name: {zookeeper.name}</ul>
            <ul>Birthday: {zookeeper.birthday}</ul>
        """
        for animal in zookeeper.animals: 
            response_body += f"<ul>Animal: {animal.name}</ul>"
        status_code = 200
    else: 
        response_body = f"""
            <ul>404 Not Found: No zookeeper with id {id} </ul>
        """
        status_code = 404

    return make_response(response_body, status_code)

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    if enclosure := db.session.get(Enclosure, id):
        response_body = f"""
            <ul>ID: {enclosure.id}</ul>
            <ul>Environment: {enclosure.environment}</ul>
            <ul>Open to Visitors: {enclosure.open_to_visitors}</ul>
        """
        for animal in enclosure.animals: 
            response_body += f"<ul>Animal: {animal.name}</ul>"
        status_code = 200
    else: 
        response_body = f"""
            <ul>404 Not Found: No enclosure with id {id} </ul>
        """
        status_code = 404

    return make_response(response_body, status_code)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
