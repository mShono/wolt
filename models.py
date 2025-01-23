from pydantic import BaseModel, Field


class DeliveryInfo(BaseModel):
    fee: int
    distance: int


class DeliveryOrderPriceInfo(BaseModel):
    total_price: int = Field(..., description="Total cost including delivery")
    small_order_surcharge: int
    cart_value: int
    delivery: DeliveryInfo
