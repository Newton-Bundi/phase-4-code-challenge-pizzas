#!/usr/bin/env python3

from faker import Faker
from random import randint, choice as rc

from app import app
from models import db, Restaurant, RestaurantPizza, Pizza

with app.app_context():
    
    fake = Faker()

    Restaurant.query.delete()
    RestaurantPizza.query.delete()
    Pizza.query.delete()

    restaurants = []
    for i in range(50):
        restaurant = Restaurant(
            name = fake.text(max_nb_chars=10),
            address = fake.address(),
        )
        restaurants.append(restaurant)

    db.session.add_all(restaurants)

    pizzas = []
    for i in range(40):
        pizza = Pizza(
            name = fake.name(),
            ingredients = fake.text(max_nb_chars=10),
        )
        pizzas.append(pizza)

    db.session.add_all(pizzas)

    restaurantpizzas = []
    for r in restaurants:
        for i in range(randint(1, 10)):
            restaurantpizza = RestaurantPizza(
                price=randint(6, 40),
                restaurant_id=randint(1, 50),
                pizza_id=randint(0, 40))
            restaurantpizzas.append(restaurantpizza)

    db.session.add_all(restaurantpizzas)
    
    db.session.commit()