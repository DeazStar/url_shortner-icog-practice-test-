FROM mysql:latest

COPY script.sql /docker-entrypoint-initdb.d/

EXPOSE 3306

CMD ["mysqld", "--bind-address=0.0.0.0"]
