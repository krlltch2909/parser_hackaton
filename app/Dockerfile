FROM python:3.9
RUN apt-get update -y
RUN apt-get upgrade -y

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get install -y locales && \
    sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

RUN apt-get -y install supervisor

WORKDIR /server

COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY . .


COPY supervisor/supervisord.conf /etc/supervisor/supervisord.conf
COPY supervisor/myproject.conf /etc/supervisor/conf.d/myproject.conf
RUN chmod +x runscript.sh

ENV LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]