#!/bin/bash
docker run --disable-content-trust -d --name "mysqlsrv" -v /tmp/toto/:/var/lib/mysql mysql-alpine
