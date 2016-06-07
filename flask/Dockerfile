#TODO: create unprivileged user, link data to mariadb container, bing logs, remove downloaded packages
FROM armhf/alpine@sha256:9f7b4923ee5e7c4ca0529431266876a70703412beee4cf72b93428393418b3bc

MAINTAINER Gary Marigliano <gary.marigliano@master.hes-so.ch>

EXPOSE 5000

RUN apk update && apk upgrade && apk add \
  python \
  py-mysqldb \
  mysql-client \
  mysql-dev \
  py-pip \
  && rm -rf /tmp/* \
  && rm -rf /var/cache/apk/*

# RUN curl -O https://bootstrap.pypa.io/get-pip.py && \
#   python get-pip.py && \
#   rm get-pip.py

RUN pip --no-cache-dir install flask MySQL-python

ENV APP_NAME iot-hello-world

CMD mkdir ${APP_NAME}

WORKDIR ${APP_NAME}

# # Use an unprivileged user called nobody
# USER nobody

ADD src app/

# CMD ["/bin/sh"]
CMD ["python", "app/main.py"]
