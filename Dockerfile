FROM python:3.8-slim

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
# Thiết lập thư mục làm việc
WORKDIR /app

# Sao chép và cài đặt các yêu cầu
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép mã nguồn ứng dụng
COPY . .

# Chạy ứng dụng
CMD ["gunicorn", "server:app", "--bind", "0.0.0.0:5000"]
