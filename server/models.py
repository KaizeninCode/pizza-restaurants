from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, MetaData, UniqueConstraint
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy()

# Association model to store many-to-many relationship between pizzas and restaurants
class RestaurantPizza(db.Model, SerializerMixin):

    __tablename__ = 'restaurant_pizzas'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    CheckConstraint('price >= 1 AND price <= 30', name='check_price_range')  # Add price validation

    # foreign key to store the restaurant_id
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))

    # foreign key to store the pizza_id
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))

    # relationship mapping a pizza to a restaurant
    pizza = db.Relationship('Pizza', back_populates='restaurant_pizzas')

    # relationship mapping a restaurant to a pizza
    restaurant = db.Relationship('Restaurant', back_populates='restaurant_pizzas')

    serialize_rules = ('-restaurant.restaurant_pizzas', '-pizza.restaurant_pizzas')


    def __repr__(self):
        return f'<Restaurant {self.restaurant.name} selling {self.pizza.name} for ${self.price}>'

class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)  # Add unique constraint and length limit
    address = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # relationship mapping restaurants to related restaurant_pizzas
    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='restaurant')

    serialize_rules = ('-restaurant_pizzas.restaurant',)


    def __repr__(self):
        return f'<Restaurant {self.name}>'


class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ingredients = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # relationship mapping restaurants to related restaurant_pizzas
    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='pizza')

    serialize_rules = ('-restaurant_pizzas.pizza',)


    def __repr__(self):
        return f'<Pizza {self.name}>'


