#!/bin/bash
docker run -d --name "mysqlsrv" -v /tmp/toto/:/var/lib/mysql mysql-alpine
