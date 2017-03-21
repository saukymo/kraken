FROM ubuntu:latest
MAINTAINER Shaobo Liu <shaobo@mkdef.com>
LABEL Description="This image is used to flask-kraken"
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
COPY .  /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["app.py"]