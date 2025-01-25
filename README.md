## DOPS
Delivery Order Price Calculator service, or DOPC for short, is an imaginary backend service which is capable of calculating the total price and price breakdown of a delivery order. DOPC integrates with the Home Assignment API to fetch venue related data required to calculate the prices.

## To run the DOPS project locally, you will need:
- Download the project from the Google disk and unzip it
- проект написан на питоне 3, работоспособность проверена на версии 3.11, требуется установленный питон 3
- Create and run a virtual environment опционально
команда
- Go to the directory with the project, install all necessary packages from requirements.txt
команда
- To run the server use the fastapi command
```
fastapi dev dops.py
```
- Or you may run the server using the uvicorn
```
uvicorn dops:app
```
- You may also run the test_dops file to make sure that the project works correctly
```
pytest
```
- To stop the server press Ctrl + C

- When the project is running, the following endpoints are available:
# Documentation
http://127.0.0.1:8000/redoc
# The main project endpoint
http://localhost:8000/api/v1/delivery-order-price
which takes the following as query parameters (all are required):
* venue_slug (string): The unique identifier (slug) for the venue from which the delivery order will be placed
* cart_value: (integer): The total value of the items in the shopping cart
* user_lat (number with decimal point): The latitude of the user's location
* user_lon (number with decimal point): The longitude of the user's location
An example request to DOPC could look like this
http://localhost:8000/api/v1/delivery-order-price?venue_slug=home-assignment-venue-helsinki&cart_value=1000&user_lat=60.17094&user_lon=24.93087
- The endpoint will return a JSON response in the following format:
{
  "total_price": 1190,
  "small_order_surcharge": 0,
  "cart_value": 1000,
  "delivery": {
    "fee": 190,
    "distance": 177
  }
}
