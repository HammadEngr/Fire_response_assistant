FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5055

CMD ["rasa", "run", "actions", "--actions", "actions", "--port", "5055"]

