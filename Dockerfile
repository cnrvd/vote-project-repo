FROM python:3.9
RUN apt-get update && apt-get install -y python3-tk

WORKDIR /app

COPY requirements.txt .
COPY app.py .
COPY templates/ ./templates/
COPY .env .

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=app.py

CMD ["flask", "run", "--host=0.0.0.0"]