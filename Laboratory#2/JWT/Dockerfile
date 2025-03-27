FROM python:3.9-slim

WORKDIR /app

COPY ./JWT/.env ./JWT/.env

COPY ./JWT/extensions.txt .
RUN pip install --no-cache-dir -r extensions.txt

COPY ./JWT/ ./JWT/
COPY ./Services/ ./Services/

CMD ["python", "-m", "JWT.JWT"]