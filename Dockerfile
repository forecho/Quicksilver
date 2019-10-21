FROM python:3.6.9
LABEL maintainer="forecho <caizhenghai@gmail.com>"
LABEL version="0.1"

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install -i https://pypi.doubanio.com/simple --no-cache-dir -r requirements.txt

COPY . /usr/src/app