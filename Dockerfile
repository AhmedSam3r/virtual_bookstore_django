FROM python:3.10.12-slim

# Set environment variables to prevent Python from writing .pyc files and ensure UTF-8 encoding
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

COPY requirements.txt /app/

# This will install the libpq-dev package, which provides pg_config and is required to build psycopg2 from source.
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . /app/
COPY .env.dev /app/.env

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
