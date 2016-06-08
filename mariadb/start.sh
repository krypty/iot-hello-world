#!/bin/bash
docker run --disable-content-trust -d --memory=512M --cap-drop=all --cap-add={SETGID,SETUID,CHOWN,DAC_OVERRIDE,KILL,FOWNER} --name "mysqlsrv" --env-file="../db_config.env" -v /tmp/toto/:/var/lib/mysql mysql-alpine
