# Sử dụng image Python 3.8
FROM python:3.8

# Thiết lập thư mục làm việc
WORKDIR /app

# Sao chép file requirements.txt vào container
COPY requirements.txt .

# Cài đặt các thư viện cần thiết
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép mã nguồn vào container
COPY . .

# Mở cổng (port) cho Flask
EXPOSE 5000

# Lệnh khởi động ứng dụng
CMD ["python", "server.py"]
