FROM --platform=$TARGETPLATFORM alpine:3.12.4 AS builder
WORKDIR /
COPY  start.sh /
RUN apk update && apk add tzdata && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
&& echo "Asia/Shanghai" > /etc/timezone \
&& apk del tzdata \
&& apk add python3 \
&& mkdir /root/ttnode \
&& crontab -r \
&& touch /root/ttnode/crontab.list \
&& crontab /root/ttnode/crontab.list \
&& wget -O /root/ttnode/get-pip.py https://bootstrap.pypa.io/get-pip.py \
&& python3 /root/ttnode/get-pip.py \
&& rm -f /root/ttnode/get-pip.py \
&& pip install urllib3 \
&& rm -rf /var/cache/apk/*
CMD ["/start.sh"]