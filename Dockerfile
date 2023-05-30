FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .

VOLUME [ ""$(pwd)"/urls.csv:/urls.csv:ro" ]

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
