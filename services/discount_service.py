from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from models import DiscountModel


def delete_discount_service(db: Session, discount_id: int):
    # Quy tắc 1: kiểm tra mã giảm giá tồn tại (và chưa bị xóa mềm trước đó)
    discount = (
        db.query(DiscountModel)
        .filter(DiscountModel.id == discount_id, DiscountModel.is_deleted == False)
        .first()
    )

    if not discount:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mã giảm giá không tồn tại trong hệ thống"
        )

    # Sáng tạo (1): không cho xóa mã giảm giá đang hoạt động trong chiến dịch
    if discount.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Không thể xóa mã giảm giá đang hoạt động. Vui lòng vô hiệu hóa trước khi xóa."
        )

    deleted_info = {
        "id": discount.id,
        "code": discount.code,
        "discount_percent": discount.discount_percent
    }

    try:
        # Quy tắc 2 & Sáng tạo (2): chỉ "xóa" khi đã tìm thấy, dùng xóa mềm
        discount.is_deleted = True
        # Sáng tạo (3): ghi lại thời điểm xóa
        discount.deleted_at = datetime.now()

        # Quy tắc 3: bắt buộc commit để lưu thay đổi xuống MySQL
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Lỗi hệ thống khi xóa mã giảm giá"
        )

    return deleted_info