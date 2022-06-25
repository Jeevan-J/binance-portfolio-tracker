FROM python:3.8-slim

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY app/ /
WORKDIR /app/

EXPOSE 80
CMD gunicorn -b 0.0.0.0:80 dashboard:server