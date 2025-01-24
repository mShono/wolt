from http import HTTPStatus
from fastapi.testclient import TestClient

from dops import app

client = TestClient(app)

url = "http://127.0.0.1:8000/api/v1/delivery-order-price"


def test_default():
    params = {
        "venue_slug": "home-assignment-venue-helsinki",
        "cart_value": 1000,
        "user_lat": 60.17094,
        "user_lon": 24.93087
    }

    response = client.get(url, params=params)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "total_price": 1190.0,
        "small_order_surcharge": 0,
        "cart_value": 1000,
        "delivery": {
            "fee": 190.0,
            "distance": 177
        }
    }


def test_long_distance():
    params = {
        "venue_slug": "home-assignment-venue-helsinki",
        "cart_value": 1000,
        "user_lat": 60.19894,
        "user_lon": 24.93087
    }

    response = response = client.get(url, params=params)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"detail":"The distance is too long, delivery is not possible"}


def test_venue_slug_missing():
    params = {
        "cart_value": 1000,
        "user_lat": 60.17094,
        "user_lon": 24.93087
    }

    response = response = client.get(url, params=params)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json() == {"detail":[{"type":"missing","loc":["query","venue_slug"],"msg":"Field required","input":None}]}


def test_venue_slug_is_not_home_api():
    params = {
        "venue_slug": 10,
        "cart_value": 1000,
        "user_lat": 60.17094,
        "user_lon": 24.93087
    }

    response = response = client.get(url, params=params)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail":"Venue '10' not found"}


def test_cart_value_is_not_int():
    params = {
        "venue_slug": "home-assignment-venue-helsinki",
        "cart_value": "bb",
        "user_lat": 60.17094,
        "user_lon": 24.93087
    }

    response = response = client.get(url, params=params)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json() == {"detail":[{"type":"int_parsing","loc":["query","cart_value"],"msg":"Input should be a valid integer, unable to parse string as an integer","input":"bb"}]}


def test_cart_value_is_neg_int():
    params = {
        "venue_slug": "home-assignment-venue-helsinki",
        "cart_value": -35,
        "user_lat": 60.17094,
        "user_lon": 24.93087
    }

    response = response = client.get(url, params=params)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json() == {"detail":[{"type":"greater_than_equal","loc":["query","cart_value"],"msg":"Input should be greater than or equal to 0","input":"-35","ctx":{"ge":0}}]}


def test_user_cord_is_not_int():
    params = {
        "venue_slug": "home-assignment-venue-helsinki",
        "cart_value": 1000,
        "user_lat": "bb",
        "user_lon": "bb"
    }

    response = response = client.get(url, params=params)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json() == {"detail":[
        {"type":"float_parsing","loc":["query","user_lat"],"msg":"Input should be a valid number, unable to parse string as a number","input":"bb"},
        {"type":"float_parsing","loc":["query","user_lon"],"msg":"Input should be a valid number, unable to parse string as a number","input":"bb"}
    ]}


def test_user_cord_value_is_too_big():
    params = {
        "venue_slug": "home-assignment-venue-helsinki",
        "cart_value": 1000,
        "user_lat": 91,
        "user_lon": 182
    }

    response = response = client.get(url, params=params)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json() == {"detail":[
        {"type":"less_than_equal","loc":["query","user_lat"],"msg":"Input should be less than or equal to 90","input":"91","ctx":{"le":90.0}},
        {"type":"less_than_equal","loc":["query","user_lon"],"msg":"Input should be less than or equal to 180","input":"182","ctx":{"le":180.0}}
    ]}


def test_user_cord_value_is_too_small():
    params = {
        "venue_slug": "home-assignment-venue-helsinki",
        "cart_value": 1000,
        "user_lat": -91,
        "user_lon": -182
    }

    response = response = client.get(url, params=params)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json() == {"detail":[{"type":"greater_than_equal","loc":["query","user_lat"],"msg":"Input should be greater than or equal to -90","input":"-91","ctx":{"ge":-90.0}},{"type":"greater_than_equal","loc":["query","user_lon"],"msg":"Input should be greater than or equal to -180","input":"-182","ctx":{"ge":-180.0}}]}

