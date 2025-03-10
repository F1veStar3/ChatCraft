FROM python:3.13

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

CMD ["sh", "-c", "python manage.py migrate && uvicorn core.asgi:application --host 0.0.0.0 --port 8000"]
