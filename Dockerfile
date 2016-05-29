#TODO: create unprivileged user, link data to mariadb container, bing logs, remove downloaded packages
FROM armhf/alpine@sha256:9f7b4923ee5e7c4ca0529431266876a70703412beee4cf72b93428393418b3bc

MAINTAINER Gary Marigliano <gary.marigliano@master.hes-so.ch>

RUN apk update && apk upgrade && apk add \
  python3 \
  curl \
  && rm -rf /tmp/* \
  && rm -rf /var/cache/apk/*

RUN curl -O https://bootstrap.pypa.io/get-pip.py && \
  python3 get-pip.py && \
  rm get-pip.py

RUN pip --no-cache-dir install Flask

ENV APP_NAME iot-hello-world

CMD mkdir ${APP_NAME}

WORKDIR ${APP_NAME}

# Use an unprivileged user called nobody
USER nobody

ADD src .

EXPOSE 5000

CMD ["python3", "main.py"]
