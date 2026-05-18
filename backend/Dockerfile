FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
EXPOSE 8000

CMD ["sh", "-lc", "python manage.py migrate --noinput && gunicorn bmi_monitor.wsgi:application --bind 0.0.0.0:8000"]
