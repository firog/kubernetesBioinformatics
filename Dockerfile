FROM ubuntu:16.04
MAINTAINER Olof Markstedt <olofmarkstedt@gmail.com>

ENV INSTALL_PATH /scalablecloudcommunity
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH
# RUN apt-get update && apt-get -y install ncbi-blast+ && apt-get -y install parallel && \
RUN apt-get update && apt-get -y install python3-pip && apt-get -y install default-jre && apt-get -y install parallel && apt-get -y install curl
#RUN apt-get install -y nginx
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.6.4/bin/linux/amd64/kubectl
RUN mv /scalablecloudcommunity/kubectl /usr/local/bin/kubectl
RUN chmod +x /usr/local/bin/kubectl
#COPY requirements.txt requirements.txt
COPY . .
RUN pip3 install -r requirements.txt
#COPY application /etc/nginx/sites-available/application
#CMD ln -s /etc/nginx/sites-available/application /etc/nginx/sites-enabled/
#CMD service nginx restart
CMD touch $INSTALL_PATH/celery.log
CMD touch $INSTALL_PATH/celery.pid

CMD ["./run.sh"]

# apt-get -y install default-jre && apt-get -y install default-jdk
