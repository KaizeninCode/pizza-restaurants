from flask import Flask, request, jsonify
from flask_migrate import Migrate

from models import db, Restaurant, Pizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return f'<h1>Pizza Restaurants</h1>'

@app.route('/restaurants')
def get_restaurants():
    # get a list of all restaurants
    restaurants = Restaurant.query.all()

    # display the results as JSON
    res_json = [restaurant.to_dict() for restaurant in restaurants] 
    return jsonify(res_json), 200

@app.route('/restaurants/<int:id>', methods = ['GET', 'DELETE'])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return jsonify({'error':"Restaurant not found"}, 404)
    
    if request.method == 'GET':
        return jsonify(restaurant.to_dict()), 200
    
    elif request.method == 'DELETE':
        # Delete associated RestaurantPizzas
        for pizza in restaurant.pizzas:
            restaurant.pizzas.remove(pizza)
        if not restaurant:
            return jsonify({'error':'Restaurant not found'}), 404
        db.session.delete(restaurant)
        db.session.commit()
        return '', 200

@app.route('/pizzas')
def pizzas():
    # get a list pizzas from the database
    pizzas = Pizza.query.all()

    # display the results as JSON    
    return jsonify([pizza.to_dict() for pizza in pizzas]), 200

@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.json
    
    # Check if all required fields are provided
    if not all(key in data for key in ['price', 'pizza_id', 'restaurant_id']):
        return jsonify({'errors': ['Missing required fields']}), 400

    price = data['price']
    pizza_id = data['pizza_id']
    restaurant_id = data['restaurant_id']

    # Validate price range
    if not (1 <= price <= 30):
        return jsonify({'errors': ['Price must be between 1 and 30']}), 400

    # Check if Pizza and Restaurant exist
    pizza = Pizza.query.get(pizza_id)
    restaurant = Restaurant.query.get(restaurant_id)

    if not pizza or not restaurant:
        return jsonify({'errors': ['Pizza or Restaurant not found']}), 404

    # # Create and add RestaurantPizza entry
    # # restaurant_pizza = RestaurantPizza(price=price, pizza=pizza, restaurant=restaurant)
    # db.session.add(restaurant_pizza)
    # db.session.commit()

    return jsonify(pizza.to_dict()), 201


if __name__ == '__main__':
    app.run(port=5555,debug=True)