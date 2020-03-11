#
# httpie-edgegrid Dockerfile
#

FROM alpine:latest
RUN apk update && apk upgrade
RUN apk -uv add --no-cache python3 py3-pip build-base musl python3-dev libffi libffi-dev openssl-dev jq
RUN pip3 install --no-cache-dir 'urllib3==1.22' --force-reinstall
RUN pip3 install --no-cache-dir --upgrade pip
RUN pip3 install --no-cache-dir cryptography httpie-edgegrid

RUN rm -rf /var/cache/apk/*
