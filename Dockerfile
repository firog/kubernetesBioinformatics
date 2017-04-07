FROM ubuntu:16.04
MAINTAINER Olof Markstedt <olofmarkstedt@gmail.com>

ENV INSTALL_PATH /scalablecloudcommunity
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH
RUN apt-get update && apt-get -y install ncbi-blast+ && apt-get -y install parallel && \
apt-get -y install python3-pip && apt-get -y install default-jre
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

CMD touch $INSTALL_PATH/celery.log
CMD touch $INSTALL_PATH/celery.pid
CMD ["./run.sh"]

# apt-get -y install default-jre && apt-get -y install default-jdk
