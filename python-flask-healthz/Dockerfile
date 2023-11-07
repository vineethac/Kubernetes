FROM ubuntu
RUN apt-get update
RUN apt-get install -y vim
RUN apt-get install -y curl
RUN apt-get install -y python3
RUN apt-get install -y pip
RUN pip3 install flask flask-healthz
COPY app.py /opt/app.py
ENTRYPOINT python3 /opt/app.py
