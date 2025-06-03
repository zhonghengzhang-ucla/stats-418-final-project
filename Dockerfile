FROM python:3.12-slim

WORKDIR /server

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "server.py"]