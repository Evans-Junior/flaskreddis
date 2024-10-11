FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y libpq-dev gcc && pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
