FROM alpine:latest
LABEL maintainer="DAD Team Chicago <DADTeamChicago@lego.com>"

RUN apk update && apk upgrade

RUN apk add --update python3 py3-pip build-base musl python3-dev libffi libffi-dev openssl-dev jq

RUN pip3 install 'urllib3==1.22' --force-reinstall
RUN pip3 install --upgrade pip
RUN pip3 install cryptography httpie-edgegrid

RUN rm -rf /var/cache/apk/*
