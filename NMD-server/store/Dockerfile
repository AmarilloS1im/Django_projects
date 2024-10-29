FROM python:3.12
LABEL author=AmarilloSlim
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
RUN apt-get update -y
RUN apt-get upgrade -y
RUN pip install --upgrade pip
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
WORKDIR /app
COPY . .
RUN chmod -R 777 ./