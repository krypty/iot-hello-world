#TODO: create unprivileged user, link data to mariadb container, bing logs, remove downloaded packages
FROM armhf/alpine@sha256:9f7b4923ee5e7c4ca0529431266876a70703412beee4cf72b93428393418b3bc

MAINTAINER Gary Marigliano <gary.marigliano@master.hes-so.ch>

EXPOSE 3306

ENV ROOT_PWD very_secured_password

RUN apk update && apk upgrade && apk add \
  mysql \
  mysql-client \
  && rm -rf /tmp/* \
  && rm -rf /var/cache/apk/*

# RUN '/usr/bin/mysqladmin' -u root password '$ROOT_PWD'

VOLUME ["/var/lib/mysql"]

# Use an unprivileged user called mysql
# USER mysql

ADD scripts/* /scripts/
RUN chmod 700 /scripts/startup.sh && \
  chmod 700 /scripts/create_db.sh

# TODO pass env var to this script
CMD ["/scripts/startup.sh"]
