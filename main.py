"""
1. Input / Output
Input: discount_id (int) từ URL path — DELETE /discounts/{discount_id}
Output thành công (200):
json{
  "message": "Xóa mã giảm giá thành công",
  "data": {
    "id": 1,
    "code": "SALE50",
    "discount_percent": 50
  }
}
Output thất bại (404):
json{
  "detail": "Mã giảm giá không tồn tại trong hệ thống"
}
2. Hai giải pháp
Giải pháp 1 — Xóa cứng (Hard Delete):
Tìm bản ghi bằng db.query(...).filter(...).first(), nếu tồn tại thì db.delete(obj) + db.commit(). Dữ liệu bị xóa vĩnh viễn khỏi MySQL.
Giải pháp 2 — Xóa mềm (Soft Delete):
Thêm cột is_deleted (Boolean) và deleted_at (DateTime). Khi "xóa", chỉ cập nhật is_deleted = True, deleted_at = datetime.now() rồi db.commit(). Dữ liệu vẫn còn trong DB nhưng bị ẩn khỏi các truy vấn nghiệp vụ.
Phần 2: So sánh & Lựa chọn
Tiêu chíGiải pháp 1 (Hard Delete)Giải pháp 2 (Soft Delete)Độ dễ hiểuCao, đơn giảnTrung bình, cần thêm điều kiện filter is_deleted ở mọi querySố lượng code cần viếtÍtNhiều hơn (thêm cột, thêm điều kiện lọc)Khả năng kiểm soát lỗiTốtTốtCó kiểm tra mã tồn tại không?CóCóKhôi phục dữ liệu nếu xóa nhầmKhông thểCó thể (chỉ cần set lại is_deleted = False)Truy vết lịch sử (mã đã dùng cho đơn hàng nào)Mất dữ liệu tham chiếu, có thể lỗi FK với bảng OrderGiữ nguyên, không phá vỡ liên kết dữ liệuPhù hợp với hệ thống thương mại điện tửRủi ro (mã giảm giá có thể đã gắn với đơn hàng cũ)Phù hợp hơn (an toàn dữ liệu, có thể audit)Mức độ phù hợp với SQLAlchemy ORMPhù hợpPhù hợpKhả năng tách logic vào ServiceDễDễ
Lựa chọn: Giải pháp 2 — Soft Delete
Lý do:

Mã giảm giá trong hệ thống thương mại điện tử thường đã được áp dụng vào các đơn hàng cũ; nếu xóa cứng có thể gây lỗi ràng buộc khóa ngoại (FK) hoặc mất dữ liệu lịch sử cần cho báo cáo/đối soát.
Marketing có thể xóa nhầm (một trong các lý do đề bài nêu: "tạo nhầm", "nhập sai") → soft delete cho phép khôi phục dễ dàng.
Đáp ứng luôn yêu cầu sáng tạo mở rộng (2) và (3) của đề bài mà không cần thêm bảng phụ.
Vẫn tuân thủ đầy đủ Quy tắc 1–4: kiểm tra tồn tại, chỉ "xóa" khi tìm thấy, commit, và logic đặt trong Service.
"""
from fastapi import FastAPI
from database import Base, engine
from routers import discount_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-commerce Discount API")

app.include_router(discount_router.router)

