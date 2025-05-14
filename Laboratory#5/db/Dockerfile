FROM python:3.10-slim

WORKDIR /app

COPY db/ /app/db/
COPY database/ /app/database/
COPY models/ /app/models/
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-m", "db.init_db"]