from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, MetaData
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Association table to store many-to-many relationship between pizzas and restaurants
pizza_res = db.Table(
    'RestaurantPizza',
    metadata,
    db.Column('restaurant_id', db.Integer, db.ForeignKey('restaurants.id'), primary_key=True),
    db.Column('pizza_id', db.Integer, db.ForeignKey('pizzas.id'), primary_key=True),
    db.Column('price', db.Float, nullable=False),
    CheckConstraint('price >= 1 AND price <= 30', name='check_price_range')  # Add price validation
)

class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)  # Add unique constraint and length limit
    address = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Relationship mapping the pizzas to related restaurants
    pizzas = db.relationship('Pizza', secondary=pizza_res, back_populates='restaurants')

    # @validates('name')
    # def validate_name(self, name):
    #     if len(name) > 50:
    #         raise ValueError("Restaurant name must be less than or equal to 50 characters.")
    #     return name

    def __repr__(self):
        return f'<Restaurant {self.name}>'


class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ingredients = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Relationship mapping the restaurants to related pizzas
    restaurants = db.relationship('Restaurant', secondary=pizza_res, back_populates='pizzas')

    def __repr__(self):
        return f'<Pizza {self.name}>'
