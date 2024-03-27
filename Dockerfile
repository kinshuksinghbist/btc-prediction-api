FROM python:3.9-slim AS builder
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt

FROM python:3.9-slim
WORKDIR /app
COPY . .
EXPOSE 5000
CMD ["python", "btc_api.py"]
