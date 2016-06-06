#TODO: create unprivileged user, link data to mariadb container, bing logs, remove downloaded packages
FROM alpine

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

CMD ["/scripts/startup.sh"]
