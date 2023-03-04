FROM python:3.8.2-slim-buster
RUN pip install --upgrade pip
WORKDIR /app

RUN apt-get update && apt-get install -y gcc vim
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000:8000

ENTRYPOINT [ "sh", "./devops/bootup.sh" ]