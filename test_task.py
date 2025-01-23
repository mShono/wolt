from http import HTTPStatus
import httpx

url = "http://127.0.0.1:8000/api/v1/delivery-order-price"


def test_default():
    params = {
        "venue_slug": "home-assignment-venue-helsinki",
        "cart_value": 1000,
        "user_lat": 60.17094,
        "user_lon": 24.93087
    }

    response = httpx.get(url, params=params)
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

    response = httpx.get(url, params=params)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail":"The distance is too long, delivery is not possible"}


def test_venue_slug_missing():
    params = {
        "cart_value": 1000,
        "user_lat": 60.17094,
        "user_lon": 24.93087
    }

    response = httpx.get(url, params=params)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json() == {"detail":[{"type":"missing","loc":["query","venue_slug"],"msg":"Field required","input":None}]}


def test_venue_slug_is_not_home_api():
    params = {
        "venue_slug": 10,
        "cart_value": 1000,
        "user_lat": 60.17094,
        "user_lon": 24.93087
    }

    response = httpx.get(url, params=params)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail":"Venue '10' not found"}


def test_cart_value_is_not_int():
    params = {
        "venue_slug": "home-assignment-venue-helsinki",
        "cart_value": "bb",
        "user_lat": 60.17094,
        "user_lon": 24.93087
    }

    response = httpx.get(url, params=params)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json() == {"detail":[{"type":"int_parsing","loc":["query","cart_value"],"msg":"Input should be a valid integer, unable to parse string as an integer","input":"bb"}]}


def test_cart_value_is_neg_int():
    params = {
        "venue_slug": "home-assignment-venue-helsinki",
        "cart_value": -35,
        "user_lat": 60.17094,
        "user_lon": 24.93087
    }

    response = httpx.get(url, params=params)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json() == {"detail":[{"type":"greater_than_equal","loc":["query","cart_value"],"msg":"Input should be greater than or equal to 0","input":"-35","ctx":{"ge":0}}]}


def test_user_lat_is_not_int():
    params = {
        "venue_slug": "home-assignment-venue-helsinki",
        "cart_value": 1000,
        "user_lat": "bb",
        "user_lon": 24.93087
    }

    response = httpx.get(url, params=params)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json() == {"detail":[{"type":"float_parsing","loc":["query","user_lat"],"msg":"Input should be a valid number, unable to parse string as a number","input":"bb"}]}
