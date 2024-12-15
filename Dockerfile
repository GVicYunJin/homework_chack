# 使用基础镜像
FROM python:3.9-slim

# 安装 zbar 库的依赖
RUN apt-get update && apt-get install -y \
    zbar-tools \
    libzbar0 \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制当前目录的内容到工作目录
COPY . /app

# 使用阿里云 pypi 镜像源安装依赖
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ --no-cache-dir Flask Pillow pyzbar python-barcode

# 暴露端口 44441
EXPOSE 44441

# 运行 Flask 应用
CMD ["python", "app.py"]
