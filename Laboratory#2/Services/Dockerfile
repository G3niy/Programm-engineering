FROM python:3.9-slim

WORKDIR /app

COPY ./Services/.env ./Services/.env

COPY ./Services/extensions.txt .
RUN pip install --no-cache-dir -r extensions.txt

COPY ./Services/ ./Services/

CMD ["python", "-m", "Services.OrdersAndServices"]