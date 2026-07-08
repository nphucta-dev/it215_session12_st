from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from database import Base


class DiscountModel(Base):
    __tablename__ = "discounts"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False)
    discount_percent = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)       # đang được áp dụng cho chiến dịch hay không
    is_deleted = Column(Boolean, default=False)      # Sáng tạo (2): xóa mềm
    deleted_at = Column(DateTime, nullable=True)      # Sáng tạo (3): thời điểm xóa