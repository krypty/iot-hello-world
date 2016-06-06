#/bin/ash
mysql -uroot -palpine -e "CREATE DATABASE todo_list COLLATE 'utf8_general_ci';"
mysql -uroot -palpine -e "GRANT ALL ON todo_list.* TO user@localhost IDENTIFIED BY 'password';"
mysql -uroot -palpine -e "CREATE TABLE todo_list.tbl_tasks (
  id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  title varchar(50) NOT NULL,
  description varchar(255) NOT NULL,
  done tinyint(1) NOT NULL
) COMMENT='' ENGINE='InnoDB';"
mysql -uroot -palpine -e "INSERT INTO todo_list.tbl_tasks (title, description, done)
VALUES ('My first task', 'This is my first task', '0');"
