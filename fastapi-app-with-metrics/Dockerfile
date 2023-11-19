FROM python:3.10-slim
WORKDIR /fastapi-app
RUN apt-get update
RUN apt-get install -y vim
RUN apt-get install -y curl
COPY requirements.txt .
COPY main.py .
RUN pip3 install -r requirements.txt
EXPOSE 5000
ENTRYPOINT python3 main.py
