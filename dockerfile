# Sử dụng Python 3.10 làm base image
FROM python:3.10

# Đặt thư mục làm việc trong container
WORKDIR /app

# Copy toàn bộ code vào container
COPY . /app

# Cài đặt thư viện từ requirements.txt
RUN pip install -r requirements.txt

# Mở cổng nếu dùng FastAPI (mặc định 8000)
EXPOSE 8000

# Chạy ứng dụng
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
