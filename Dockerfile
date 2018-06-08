FROM alpine:latest

RUN apk update && apk upgrade

RUN apk add --update python3 py3-pip build-base musl python3-dev libffi libffi-dev openssl-dev

RUN pip3 install --upgrade pip
RUN pip3 install cryptography
RUN pip3 install httpie-edgegrid

RUN rm -rf /var/cache/apk/*
