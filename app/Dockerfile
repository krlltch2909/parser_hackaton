FROM python:3.9
RUN apt-get update -y
RUN apt-get upgrade -y

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y locales && \
    sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

WORKDIR /server

COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

ENV LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8