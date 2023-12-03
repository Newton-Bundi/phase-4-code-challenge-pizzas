#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS

from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Index(Resource):

    def get(self):

        response_dict = {
            "index": "Welcome to the Newsletter RESTful API",
        }

        response = make_response(
            jsonify(response_dict),
            200,
        )

        return response

api.add_resource(Index, '/')

class Restaurants(Resource):

    def get(self):

        restaurants = []
        for restaurant in Restaurant.query.all():
            restaurant_dict = restaurant.to_dict()
            restaurants.append(restaurant_dict)

        response = make_response(
        restaurants,
        200
        )

        return response

    def post(self):

        data = request.get_json()

        new_restaurant = Restaurant(
            name=data['name'],
            address=data['address'],
        )

        db.session.add(new_restaurant)
        db.session.commit()

        return make_response(new_restaurant.to_dict(), 201)

api.add_resource(Restaurants, '/restaurants')

class RestaurantByID(Resource):
    def get(self, id):
        response = Restaurant.query.filter_by(id=id).first().to_dict()

        if response == None:
            response_body = {
            "error": "Restaurant not found."
            }
            response = make_response(response_body, 404)
        
        return response

    def delete(self, id):

        record = Restaurant.query.filter_by(id=id).first()

        db.session.delete(record)
        db.session.commit()

        response_dict = {"message": "record successfully deleted"}

        response = make_response(
            jsonify(response_dict),
            200
        )

        return response

api.add_resource(RestaurantByID, '/restaurants/<int:id>')


class Pizzas(Resource):

    def get(self):

        pizzas = []
        for pizza in Pizza.query.all():
            pizza_dict = pizza.to_dict()
            pizzas.append(pizza_dict)

        response = make_response(
        pizzas,
        200
        )

        return response  


    def post(self):

        data = request.get_json()

        new_pizza = Pizza(
            name=data['name'],
            ingredients=data['ingredients'],
        )

        db.session.add(new_pizza)
        db.session.commit()

        return make_response(new_pizza.to_dict(), 201)

api.add_resource(Pizzas, '/pizzas')


class RestaurantsPizzas(Resource):

    def get(self):
        restaurant_pizza = [restaurantpizza.to_dict() for restaurantpizza in RestaurantPizza.query.all()]
        return make_response(jsonify(restaurant_pizza), 200)

    def post(self):

        data = request.get_json()

        new_resturant_pizza = RestaurantPizza(
            price=data['price'],
            pizza_id=data['pizza_id'],
            restaurant_id=data['restaurant_id'],
        )

        db.session.add(new_resturant_pizza)
        db.session.commit()

        return make_response(new_resturant_pizza.to_dict(), 201)

api.add_resource(RestaurantsPizzas, '/restaurant_pizzas')


if __name__ == '__main__':
    app.run(port=5555, debug=True)