#!/usr/bin/env python3

from flask import Flask, make_response, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False


migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route('/')
def home():
    response_body = {
        'Welcome to the Hero Database!'
    }
    response = make_response(
        response_body,
        200
    )
    return response

@app.route('/heroes',methods = ['GET'])
def heroes():

    heroes = Hero.query.all()

    if request.method == 'GET':
        heroes_dict = [heroes.to_dict() for heroes in heroes]
        
        response = make_response(
            heroes_dict,
            200
        )

        return response

@app.route('/heroes/<int:id>',methods = ['GET'])
def heroes_id(id):
    hero = Hero.query.filter(Hero.id == id).first()

    if not hero:
        response_body = {
            "error": "Hero not found"
        }
        response = make_response(
            response_body,
            404
        )
        return response

    elif request.method == 'GET':
        hero_dict = hero.to_dict()
        
        response = make_response(
            hero_dict,
            200
        )

        return response
    
@app.route('/powers',methods = ['GET'])
def powers():
    powers = Power.query.all()

    if request.method == 'GET':
        power_dict = [powers.to_dict() for powers in powers]
        
        response = make_response(
            power_dict,
            200
        )

        return response
    
@app.route('/powers/<int:id>',methods = ['GET','PATCH'])
def power_id(id):
    power = Power.query.filter(Power.id == id).first()

    if not power:
        response_body = {
            "error": "Power not found"
        }
        response = make_response(
            response_body,
            404
        )
        return response

    elif request.method == 'GET':
        power_dict = power.to_dict()
        
        response = make_response(
            power_dict,
            200
        )

        return response
    
    elif request.method == 'PATCH':
        for attr in request.get_json():
            setattr(power,attr,request.get_json()[attr])
        db.session.add(power)
        db.session.commit()

        power_dict = power.to_dict()
        
        response = make_response(
            power_dict,
            200
        )

        return response
    
@app.route('/hero_powers',methods=['GET','POST'])
def hero_powers():

    if request.method == 'GET':
        hero_powers = Hero.query.all()
        hero_dict = [hero.to_dict() for hero in hero_powers]
        response = make_response(
            hero_dict,
            200
        )
        return response

    elif request.method == 'POST':
        new_hero_power = HeroPower(
            strength = request.get_json()['strength'],
            power_id = request.get_json()['power_id'],
            hero_id = request.get_json()['hero_id']
        )
        db.session.add(new_hero_power)
        db.session.commit()

        hero_power_dict = new_hero_power.to_dict()

        response = make_response(
            jsonify(hero_power_dict),
            201
        )


        return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
