Quản lý linh kiện máy tính
Giới thiệu
Đây là chương trình Quản lý linh kiện máy tính được phát triển bằng Python, sử dụng giao diện Tkinter và cơ sở dữ liệu MySQL. Chương trình hỗ trợ các chức năng sau:

Danh sách linh kiện: Quản lý thông tin linh kiện (thêm, sửa, xóa).
Tìm kiếm linh kiện: Tìm kiếm linh kiện theo tên hoặc loại.
Bán hàng: Chọn linh kiện, thêm vào giỏ hàng, và xác nhận bán.
Thống kê: Hiển thị biểu đồ số lượng linh kiện và doanh thu theo loại, cùng lịch sử bán hàng.

Chương trình được thiết kế với giao diện thân thiện, màu sắc đồng bộ và sử dụng font Arial.
Yêu cầu

Hệ điều hành: Windows (hoặc macOS/Linux, nhưng chưa được kiểm tra).
Python: Phiên bản 3.12.10 (hoặc mới hơn).
MySQL: MySQL Server 8.0 (hoặc mới hơn).
Thư viện Python:
mysql-connector-python: Để kết nối với MySQL.
matplotlib: Để vẽ biểu đồ trong tab Thống kê.


IDE (khuyến nghị): Visual Studio Code.

Cài đặt
1. Cài đặt Python và MySQL

Tải và cài Python 3.12.10 từ python.org.
Tải và cài MySQL Server 8.0 từ mysql.com.
Đảm bảo thêm Python vào PATH trong quá trình cài đặt.

2. Thiết lập cơ sở dữ liệu

Tạo cơ sở dữ liệu linhkien_maytinh trong MySQL:CREATE DATABASE linhkien_maytinh;
USE linhkien_maytinh;


Tạo các bảng cần thiết (linh_kien, ban_hang, nhap_hang). File database.sql (nếu có) chứa script tạo bảng.
Cập nhật thông tin kết nối MySQL trong file database.py:self.conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Thay bằng mật khẩu của bạn
    database="linhkien_maytinh"
)

3. Cài đặt thư viện Python

Mở terminal (PowerShell hoặc Command Prompt) trong thư mục dự án:cd D:\HK8\PYTHON_PROGRAMMING\Website_linhkien_maytinh

Cài các thư viện
pip install mysql-connector-python
pip install matplotlib

Giao diện:
Chương trình có 4 tab chính:
Danh sách linh kiện: Quản lý linh kiện (thêm, sửa, xóa).
Tìm kiếm linh kiện: Tìm kiếm theo tên hoặc loại.
Bán hàng: Chọn linh kiện, thêm vào giỏ, xác nhận bán.
Thống kê: Xem biểu đồ số lượng và doanh thu, lịch sử bán hàng.

Lưu ý:
Đảm bảo MySQL đang chạy trước khi mở chương trình.
Nếu gặp lỗi import trong IDE (như VS Code), chọn đúng Python interpreter (3.12.10) và cài lại thư viện.

Cấu trúc dự án
Website_linhkien_maytinh/
├── database.py          # Quản lý kết nối và truy vấn MySQL
├── linhkien_manager.py  # Tab Danh sách linh kiện
├── timkiem_manager.py   # Tab Tìm kiếm linh kiện
├── banhang_manager.py   # Tab Bán hàng
├── thongke_manager.py   # Tab Thống kê
├── main.py              # File chính, tích hợp các tab
└── README.md            # Tài liệu hướng dẫn

Hướng phát triển

Thêm chức năng xuất hóa đơn sau khi bán hàng.
Thêm thanh cuộn cho bảng dữ liệu lớn.
Tối ưu truy vấn MySQL để tăng hiệu suất.

Tác giả

Họ tên: Đoàn Trọng Tấn
MSSV: 21IT106
Dự án thực hiện trong môn học: Lập trình Python, Học kỳ 8, Năm 2025.

