FROM python:3.9
RUN apt-get update -y
RUN apt-get upgrade -y

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /server

COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

EXPOSE 8000
