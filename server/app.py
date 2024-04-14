from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Initialize database
migrate = Migrate(app, db)
db.init_app(app)

# Routes
@app.route('/')
def home():
    return '<h1>Pizza Restaurants</h1>'

@app.route('/restaurants')
def get_restaurants():
    restaurants = Restaurant.query.all()
    return make_response(jsonify([restaurant.to_dict() for restaurant in restaurants])), 200

@app.route('/restaurants/<int:id>')
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return make_response({'error': 'Restaurant not found'}), 404
    return make_response(jsonify(restaurant.to_dict())), 200

@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return make_response(jsonify({'error': 'Restaurant not found'})), 404
    db.session.delete(restaurant)
    db.session.commit()
    return '', 204

@app.route('/pizzas')
def get_pizzas():
    pizzas = Pizza.query.all()
    return make_response(jsonify([pizza.to_dict() for pizza in pizzas])), 200

# BONUS ENDPOINT NOT INCLUDED IN THE INSTRUCTIONS
@app.route('/restaurant_pizzas')
def get_res_pizzas():
    rp = RestaurantPizza.query.all()
    return make_response(jsonify([r.to_dict() for r in rp]))

@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.json
    required_fields = ['price', 'pizza_id', 'restaurant_id']
    if not all(field in data for field in required_fields):
        return make_response(jsonify({'error': 'Missing required fields'})), 400

    price = data['price']
    pizza_id = data['pizza_id']
    restaurant_id = data['restaurant_id']

    if not (1 <= price <= 30):
        return make_response(jsonify({'error': 'Price must be between 1 and 30'})), 400

    pizza = Pizza.query.get(pizza_id)
    restaurant = Restaurant.query.get(restaurant_id)
    
    if not pizza:
        return make_response(jsonify({'error': 'Pizza not found'})), 404
    if not restaurant:
        return make_response(jsonify({'error': 'Restaurant not found'})), 404

    restaurant_pizza = RestaurantPizza(price=price, pizza=pizza, restaurant=restaurant)
    db.session.add(restaurant_pizza)
    db.session.commit()

    return make_response(jsonify(pizza.to_dict())), 201

if __name__ == '__main__':
    app.run(port=5555, debug=True)
