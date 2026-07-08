from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import DeleteDiscountResponse
from services.discount_service import delete_discount_service

router = APIRouter(prefix="/discounts", tags=["Discounts"])


# Quy tắc 4: Router chỉ gọi Service, không chứa logic xử lý
@router.delete("/{discount_id}", response_model=DeleteDiscountResponse)
def delete_discount(discount_id: int, db: Session = Depends(get_db)):
    deleted_discount = delete_discount_service(db, discount_id)
    return {
        "message": "Xóa mã giảm giá thành công",
        "data": deleted_discount
    }