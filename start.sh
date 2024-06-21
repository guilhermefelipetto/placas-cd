#!/bin/bash

# Inicializa o MariaDB
mysqld_safe --skip-grant-tables &
sleep 10

mysql -u root -p"$MYSQL_ROOT_PASSWORD" < ./database_scripts/database.sql

python ./main.py &

exec "$@"
