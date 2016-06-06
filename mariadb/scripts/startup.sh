#!/bin/ash
# if [[ `ls /var/lib/mysql | wc -l`  == "0" ]]; then
#   /usr/bin/mysql_install_db --user=mysql
# fi
# /usr/bin/mysqld_safe --datadir="/var/lib/mysql"

if [[ `ls /var/lib/mysql | wc -l`  == "0" ]]; then
  mysql_install_db --user=mysql
  mysqld_safe --datadir="/var/lib/mysql" &
  sleep 15s
  mysqladmin -u root password alpine

  # create database with default tasks
  ash /scripts/create_db.sh

  killall mysqld

  sleep 10s
fi
mysqld_safe --datadir="/var/lib/mysql"
