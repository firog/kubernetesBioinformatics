FROM python:3.5-alpine

MAINTAINER Olof Markstedt <olofmarkstedt@gmail.com>

ENV INSTALL_PATH /scalablecloudcommunity
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH
COPY requirements.txt requirements.txt
#RUN apk add --update python python-dev py-pip && pip install virtualenv && rm -rf /var/cache/apk/*
RUN pip install -r requirements.txt
COPY . .

#RUN pip install -r /usr/src/manage/requirements.txt
EXPOSE 8000
RUN chmod +x run.sh
CMD ["./run.sh"]
