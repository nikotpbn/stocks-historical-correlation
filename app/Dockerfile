FROM python:3.13-alpine3.22

WORKDIR /app
COPY requirements.txt .

RUN apk add build-base
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["python", "main.py"]