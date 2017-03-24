FROM python:3.4-wheezy

MAINTAINER Olof Markstedt <olofmarkstedt@gmail.com>

ENV INSTALL_PATH /scalablecloudcommunity
#ENV C_FORCE_ROOT=1
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH
RUN apt-get update && apt-get -y install ncbi-blast+ && apt-get -y install parallel
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

#CMD python manage.py runserver --host 0.0.0.0 --port 5000
CMD mkdir -p $HOME/run/celery/pid
CMD mkdir -p $HOME/log/celery/log
CMD ["./run.sh"]

#CMD gunicorn -b 0.0.0.0:8000 --access-logfile - "app:create_app()"


#RUN apk add --update python python-dev py-pip && pip install virtualenv && rm -rf /var/cache/apk/*
#RUN pip install -r /usr/src/manage/requirements.txt
#EXPOSE 8000
#RUN chmod +x run.sh
#CMD ["./run.sh"]
