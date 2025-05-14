FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY users/ /app/users/
COPY database/ /app/database/
COPY models/ /app/models/
COPY authentication/ /app/authentication/

CMD ["python", "-m", "users.User_Service"]