FROM python:3.11

WORKDIR /my_bot
    COPY . .

RUN apt-get update
RUN apt-get -y install postgresql-client
RUN chmod +x wait-for-postgres.sh

RUN pip install -r requirements.txt