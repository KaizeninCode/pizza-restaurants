from app import app
from models import Pizza, Restaurant, db, RestaurantPizza


with app.app_context():

    # Delete all rows in all tables
    RestaurantPizza.query.delete()
    Restaurant.query.delete()
    Pizza.query.delete()

    db.create_all()
    
    # Create restaurants
    dominion_pizza = Restaurant(name='Dominion Pizza', address='Good Italian, Ngong Road, 5th Avenue')
    pizza_hut = Restaurant(name='Pizza Hut', address='Westgate Mall, Mwanzi Road, Nrb 100')
    bigknife = Restaurant(name='Big Knife', address='99 Jabavu Lane, Nairobi')
    spur = Restaurant(name='Spur', address='James Gichuru Road, Westlands, Nairobi')

    # Create pizzas
    cheese = Pizza(name='Cheese', ingredients='Dough, Tomato Sauce, Cheese')
    pepperoni = Pizza(name='Pepperoni', ingredients='Dough, Tomato Sauce, Cheese, Pepperoni')

    # many-to-many relationship between pizzas and restaurants through RestaurantPizza
    rp1 = RestaurantPizza(price=9.95, pizza=cheese, restaurant=bigknife)
    rp2 = RestaurantPizza(price=11.95, pizza=pepperoni, restaurant=spur)
    rp3 = RestaurantPizza(price=9.95, pizza=cheese, restaurant=dominion_pizza)
    rp4 = RestaurantPizza(price=9.95, pizza=cheese, restaurant=pizza_hut)

    # Add objects to session and commit
    db.session.add_all([dominion_pizza, pizza_hut, cheese, pepperoni, rp1, rp2, rp3, rp4])
    db.session.commit()
