FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
EXPOSE 8000

CMD ["sh", "-lc", "python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn bmi_monitor.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]
