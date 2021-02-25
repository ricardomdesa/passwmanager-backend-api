#FROM python:3
FROM python:3.8-slim-buster

EXPOSE 5000

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY DB_Manager.py .

CMD [ "python", "app.py" ]
