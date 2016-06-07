#!/bin/bash
docker run --disable-content-trust -d --name "mysqlsrv" --env-file="../db_config.env" -v /tmp/toto/:/var/lib/mysql mysql-alpine
