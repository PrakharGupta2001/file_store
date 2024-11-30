FROM python:3.9-slim

WORKDIR /app

COPY ./server /app/server
COPY requirements.txt /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "8000"]
