FROM python:3.11

WORKDIR /my_bot

COPY . .

RUN apt-get update && \
    apt-get -y install postgresql-client && \
    chmod +x wait-for-postgres.sh

RUN pip install -r requirements.txt
