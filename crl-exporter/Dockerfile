FROM python:3.9.18-alpine3.18

LABEL NAME="crl_exporter"
LABEL maintainer=" Kirill Borisov ochanoboy@gmail.com"

# Envs
ENV TZ=Asia/Almaty
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
ENV USERNAME=*****
ENV PASSWORD=*****
ENV API_URLS=*****


# SSL certificates (optional)
COPY ./some_crt.crt /usr/local/share/ca-certificates/some_crt.cer
COPY ./sub_some.crt /usr/local/share/ca-certificates/sub_some.cer

# Working dir
WORKDIR /opt/crl_exporter
COPY . /opt/crl_exporter

# Proxy for repo alpine and pip (optional)
RUN echo "https://my-prx.com/repository/apk-proxy/alpine/v3.12/main" > /etc/apk/repositories && \
    echo "https://my-prx.com/repository/apk-proxy/alpine/v3.12/community" >> /etc/apk/repositories && \
	echo -e "[global]\ntimeout=180\nindex=https://my-prx.com/repository/pypi-proxy/pypi\nindex-url=https://my-prx.com/repository/pypi-proxy/simple\ntrusted-host=my-prx.com" > /etc/pip.conf


# Packages/libs
RUN set -x; buildDeps="gcc python3-dev musl-dev libffi-dev openssl openssl-dev rust cargo ca-certificates tzdata" \
    && apk --no-cache add --update $buildDeps \
    && python3 -m pip install -r requirements.txt \
	&& apk del $buildDeps                                                                                            #removes the development dependencies keep it smaller)

# Ports
EXPOSE 8000 8001

# Move data to stdout/stderr without baffering (optional)
ENV PYTHONUNBUFFERED=1 

# Run
CMD ["python", "/opt/crl_exporter/setup.py"]