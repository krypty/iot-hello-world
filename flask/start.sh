#/bin/bash
docker run --disable-content-trust -it --cap-drop=all --memory=128MB -p 5000:5000 --link mysqlsrv:mysqlsrv --rm --env-file="../db_config.env" iot-hello-world
