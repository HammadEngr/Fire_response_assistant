FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# RUN python manage.py collectstatic --noinput

EXPOSE 8000

# for dev
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# for production
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "config.wsgi:application"]
