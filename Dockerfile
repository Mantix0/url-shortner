FROM python:3.10

WORKDIR /

COPY ./app /app

COPY requirements.txt .
COPY alembic.ini .

RUN pip install --no-cache-dir -r requirements.txt
