from pydantic import BaseModel


class DiscountOut(BaseModel):
    id: int
    code: str
    discount_percent: float

    class Config:
        from_attributes = True


class DeleteDiscountResponse(BaseModel):
    message: str
    data: DiscountOut