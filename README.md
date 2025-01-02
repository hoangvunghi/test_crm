# Django CRM

Hệ thống CRM đơn giản được xây dựng bằng Django Framework, bao gồm các chức năng quản lý khách hàng, sản phẩm, nhân sự và bảng công việc.

## Tính năng chính

- Quản lý khách hàng (CRUD)
- Quản lý sản phẩm (CRUD) 
- Quản lý nhân sự (CRUD)
- Bảng công việc (với chức năng lọc theo trạng thái và nhân sự)
- Hệ thống xác thực JWT
- Tài liệu API với Swagger
- Trang quản trị Admin tùy chỉnh

## Yêu cầu hệ thống

- Python 3.8 trở lên
- Django 4.x
- PostgreSQL (hoặc SQLite cho môi trường phát triển)

## Cài đặt và Chạy

### 1. Clone dự án

```bash
git clone https://github.com/hoangvunghi/test_crm.git
cd test_crm
```

### 2. Tạo môi trường ảo

```bash
pip install virtualenv
virtualenv env

# Kích hoạt môi trường ảo
# Windows
env\Scripts\activate
# macOS/Linux
source env/bin/activate
```

### 3. Cài đặt các gói phụ thuộc

```bash
pip install -r requirements.txt
```

### 4. Cấu hình cơ sở dữ liệu

```bash
python manage.py migrate
```

### 5. Tạo tài khoản admin

```bash
python manage.py createsuperuser
```

### 6. Chạy server

```bash
python manage.py runserver
```

Truy cập ứng dụng tại: http://localhost:8000

## API Endpoints

### Xác thực
- POST /api/auth/register/ - Đăng ký tài khoản
- POST /api/auth/login/ - Đăng nhập và nhận JWT token

### Khách hàng
- GET /api/customers/ - Lấy danh sách khách hàng
- POST /api/customers/ - Tạo khách hàng mới
- GET /api/customers/{id}/ - Xem chi tiết khách hàng  
- PUT /api/customers/{id}/ - Cập nhật thông tin khách hàng
- DELETE /api/customers/{id}/ - Xóa khách hàng

### Sản phẩm
- GET /api/products/ - Lấy danh sách sản phẩm
- POST /api/products/ - Thêm sản phẩm mới
- GET /api/products/{id}/ - Xem chi tiết sản phẩm
- PUT /api/products/{id}/ - Cập nhật thông tin sản phẩm 
- DELETE /api/products/{id}/ - Xóa sản phẩm

### Nhân sự
- GET /api/employees/ - Lấy danh sách nhân sự
- POST /api/employees/ - Thêm nhân sự mới
- GET /api/employees/{id}/ - Xem chi tiết nhân sự
- PUT /api/employees/{id}/ - Cập nhật thông tin nhân sự
- DELETE /api/employees/{id}/ - Xóa nhân sự

### Bảng công việc
- GET /api/tasks/ - Lấy danh sách công việc
- POST /api/tasks/ - Tạo công việc mới
- GET /api/tasks/{id}/ - Xem chi tiết công việc
- PUT /api/tasks/{id}/ - Cập nhật công việc
- DELETE /api/tasks/{id}/ - Xóa công việc
- GET /api/tasks/filter/ - Lọc công việc theo trạng thái và nhân sự

## Tài liệu API

Truy cập tài liệu API Swagger UI tại: http://localhost:8000/api/docs/

## Trang quản trị

Truy cập trang quản trị tại: http://localhost:8000/admin/

Các tính năng trong trang quản trị:
- Quản lý toàn bộ dữ liệu hệ thống
- Tìm kiếm và lọc dữ liệu nâng cao
- Xem lịch sử thay đổi
- Quản lý người dùng và phân quyền

## Bảo mật

- Sử dụng JWT (JSON Web Token) cho xác thực API
- Mã hóa mật khẩu
- Kiểm soát quyền truy cập dựa trên vai trò người dùng

## Hướng dẫn đóng góp

1. Fork dự án
2. Tạo nhánh tính năng mới (`git checkout -b feature/AmazingFeature`)
3. Commit thay đổi (`git commit -m 'Add some AmazingFeature'`)
4. Push lên nhánh (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## Giấy phép

Dự án được phân phối dưới giấy phép MIT. Xem `LICENSE` để biết thêm thông tin.