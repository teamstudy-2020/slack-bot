FROM ubuntu:18.04

MAINTAINER TeamStudy <dlqpdlzhfldk2020@gmail.com>

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

COPY ./requirements.txt /app/requirements.txt

# Docker 이미지 내부 run 명령어 실행되는 dir
WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

CMD ["/app/init.sh"]
