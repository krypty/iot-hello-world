#/bin/ash

# Create db user
mysql -uroot -p$MYSQL_ROOT_PASSWORD -e "CREATE USER '$MYSQL_USERNAME'@'localhost' IDENTIFIED BY '$MYSQL_PASSWORD';"
mysql -uroot -p$MYSQL_ROOT_PASSWORD -e "GRANT ALL PRIVILEGES ON *.* TO '$MYSQL_USERNAME'@'localhost' WITH GRANT OPTION;"
mysql -uroot -p$MYSQL_ROOT_PASSWORD -e "CREATE USER '$MYSQL_USERNAME'@'%' IDENTIFIED BY '$MYSQL_PASSWORD';"
mysql -uroot -p$MYSQL_ROOT_PASSWORD -e "GRANT ALL PRIVILEGES ON *.* TO '$MYSQL_USERNAME'@'%' WITH GRANT OPTION;"

# Create db
mysql -uroot -p$MYSQL_ROOT_PASSWORD -e "CREATE DATABASE $MYSQL_DB COLLATE 'utf8_general_ci';"
mysql -uroot -p$MYSQL_ROOT_PASSWORD -e "CREATE TABLE $MYSQL_DB.$TASKS_TABLE (
  id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  title varchar(50) NOT NULL,
  description varchar(255) NOT NULL,
  done tinyint(1) NOT NULL
) COMMENT='' ENGINE='InnoDB';"

# Fill db with default entry
mysql -uroot -p$MYSQL_ROOT_PASSWORD -e "INSERT INTO $MYSQL_DB.$TASKS_TABLE (title, description, done) VALUES ('My first task', 'This is my first task', '0');"

mysql -uroot -p$MYSQL_ROOT_PASSWORD -e "INSERT INTO $MYSQL_DB.$TASKS_TABLE (title, description, done) VALUES ('My second task', 'This is my second task', '1');"
