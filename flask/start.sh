#/bin/bash
docker run --disable-content-trust -it -p 5000:5000 --link mysqlsrv:mysqlsrv --rm iot-hello-world
