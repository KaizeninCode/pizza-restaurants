# PIZZA RESTAURANTS - PHASE 4 WEEK 1 CODE CHALLENGE

- In this code challenge, I was tasked with building a Flask API for a restaurant domain.

## MODELS
These were the required models:
- A `Restaurant` that has many `Pizza`s through `RestaurantPizzas`.
- A `Pizza` that has many `Restaurant`s through `RestaurantPizzas`.
- A `RestaurantPizza` model that belongs to both a `Restaurant` and a `Pizza`.

## VALIDATIONS
1. To the `RestaurantPizza` model:
   - must have a `price` that is between 1 and 30
2. To the `Restaurant`  model:
   - must have a name less than 50 words in length
   - must have a unique name

## ROUTES
These were the required routes/endpoints:
- GET/restaurants
- GET/restaurants/:id
- DELETE/restaurants/:id
- GET/pizzas
- POST/restaurant_pizzas
I added an additional endpoint (GET/pizza_restaurants) because I felt it was logical to be able to see whatever information is stored at that endpoint.
