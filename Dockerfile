FROM python:3.11

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN pip install pandas  

COPY . .

EXPOSE 5000
CMD ["python", "btc_api.py"]
