# DOPS
Delivery Order Price Calculator service, or DOPC for short, is an imaginary backend service which is capable of calculating the total price and price breakdown of a delivery order. DOPC integrates with the Home Assignment API to fetch venue related data required to calculate the prices.

## To run the DOPS project locally, you will need:
- Download the project from the Google disk and unzip it
- The project is written in python 3, functionality is tested on version 3.11, the installed python 3 is required
- Create and run a virtual environment - optional
```
python -m -venv venv

python source venv/Scripts/activate
```
- Go to the directory with the project, install all necessary packages from requirements.txt
```
pip install -r requirements.txt
```
- To run the server use the fastapi command
```
fastapi dev dops.py
```
- Or you may run the server using the uvicorn
```
uvicorn dops:app
```
- To stop the server press Ctrl + C


## Tests

The tests for the project are written on pytest. To run them, use the command
```
pytest
```

## When the project is running, the following endpoints are available:
- Documentation
http://127.0.0.1:8000/redoc
- The main project endpoint
http://localhost:8000/api/v1/delivery-order-price
which takes the following as query parameters (all are required):
  * venue_slug (string): The unique identifier (slug) for the venue from which the delivery order will be placed
  * cart_value: (integer): The total value of the items in the shopping cart
  * user_lat (number with decimal point): The latitude of the user's location
  * user_lon (number with decimal point): The longitude of the user's location
An example request to DOPC could look like this
http://localhost:8000/api/v1/delivery-order-price?venue_slug=home-assignment-venue-helsinki&cart_value=1000&user_lat=60.17094&user_lon=24.93087

The endpoint will return a JSON response in the following format:
```json
{
  "total_price": 1190,
  "small_order_surcharge": 0,
  "cart_value": 1000,
  "delivery": {
    "fee": 190,
    "distance": 177
  }
}
```
