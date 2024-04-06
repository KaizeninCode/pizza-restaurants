from app import app
from models import Pizza, Restaurant

with app.app_context():
    Pizza.query.delete()
    Restaurant.query.delete()

    pizzas = []
    pizzas.append(Pizza(name='Cheese', ingredients='Dough, Tomato Sauce, Cheese'))
    pizzas.append(Pizza(name='Pepperoni', ingredients='Dough, Tomato Sauce, Cheese, Pepperoni'))

    restaurants = []
    restaurants.append(Restaurant(name='Dominion Pizza'))
    restaurants.append(Restaurant(name='Pizza Hut'))