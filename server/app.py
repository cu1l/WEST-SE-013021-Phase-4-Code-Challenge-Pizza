#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api

from models import db, Restaurant, RestaurantPizza, Pizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route('/restaurants')
def restaurants():
    restaurants_dict = [rest.to_dict(rules=('-restaurantpizzas')) for rest in Restaurant.query.all()]
    return restaurants_dict

@app.route('/restaurants/<int:id>', methods=['GET', 'DELETE'])
def restaurant_get_id(id):
    restaurant = Restaurant.query.filter_by(id=id).first()
    if request.method == 'GET':
        return restaurant.to_dict(rules=('-restaurantpizzas'))
    if request.method == 'DELETE':
        db.session.delete(restaurant)
        db.session.commit()
        res = make_response("", 204)
        return res
    if restaurant is None:
        body = {"error": "404: Restaurant not found"}
        res = make_response(body, 404)
        return res
    
@app.route('/pizzas')
def pizzas():
    pizza_dict = [pizza.to_dict() for pizza in Pizza.query.all()]
    return pizza_dict

@app.route("/restaurant_pizzas")
def restaurantpizzas():
    try:
        app_json = request.get_json()
        new_app = RestaurantPizza(
            price = app_json['price'],
            restaurant_id = app_json['restaurant_id'],
            pizza_id = app_json['pizza_id']
        )
    except ValueError:
        return make_response({"error": "Validation error"}, 400)
    
    db.session.add(new_app)
    db.session.commit()
    dict_new = new_app.to_dict(rules=('-restaurant_id', '-pizza_id'))
    res = make_response(dict_new, 201)
    return res

if __name__ == '__main__':
    app.run(port=5555, debug=True)
