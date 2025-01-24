from fastapi import FastAPI, HTTPException, Query
import httpx
from geopy import distance

from models import DeliveryOrderPriceInfo


app = FastAPI()
BASE_URL = "https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/"


# def response_check(static_dynamic, venue_slug):
#     for info in static_dynamic:
#         if isinstance(info, httpx.Response) and info.is_error:
#             raise HTTPException(status_code=404, detail=f"Venue '{venue_slug}' not found")


async def fetch_venue_data(venue_slug: str):
    async with httpx.AsyncClient() as client:
        static = await client.get(f"{BASE_URL}{venue_slug}/static")
        dynamic = await client.get(f"{BASE_URL}{venue_slug}/dynamic")
        try:
            static.raise_for_status()
            dynamic.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=e.response.text
            )
    return static.json(), dynamic.json()


def calculate_distance(venue_cords, user_cords):
    return int(distance.distance(venue_cords, user_cords).meters)

def calculate_delivery_fee(base_price, distance_ranges, distance):
    for range in distance_ranges:
        if range["min"] <= distance <= range["max"]:
            delivery_fee = base_price + range["a"] + range["b"] * round(distance / 10)
            return delivery_fee
    raise HTTPException(status_code=520, detail="The distance is too long, delivery is not possible")


@app.get(
        "/api/v1/delivery-order-price",
        response_model=DeliveryOrderPriceInfo
)
async def get_delivery_order_price(
    venue_slug: str = Query(...),
    cart_value: int = Query(..., ge=0),
    user_lat: float = Query(..., ge=-90, le=90, description="user's latitude"),
    user_lon: float = Query(..., ge=-180, le=180, description="user's longitude")
):
    static_data, dynamic_data = await fetch_venue_data(venue_slug)
    try:
        venue_cords_lon, venue_cords_lat = static_data["venue_raw"]["location"]["coordinates"]
        delivery_specs = dynamic_data["venue_raw"]["delivery_specs"]
    except KeyError as e:
        raise HTTPException(
            status_code=503,
            detail=f"KeyError. Key {e.args[0]} is not found"
        )

    distance = calculate_distance((venue_cords_lat, venue_cords_lon), (user_lat, user_lon))

    order_min = delivery_specs["order_minimum_no_surcharge"]
    small_order_surcharge = max(0, order_min - cart_value)

    base_price = delivery_specs["delivery_pricing"]["base_price"]
    distance_ranges = delivery_specs["delivery_pricing"]["distance_ranges"]
    delivery_fee = calculate_delivery_fee(base_price, distance_ranges, distance)

    return {
        "total_price": int(cart_value + small_order_surcharge + delivery_fee),
        "small_order_surcharge": small_order_surcharge,
        "cart_value": cart_value,
        "delivery": {
            "fee": int(delivery_fee),
            "distance": distance
        }
    }
