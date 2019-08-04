# using phusion/baseimage as base image
FROM phusion/baseimage:0.9.19

# update and install apache + python

RUN apt-get update && apt-get install -y apache2 apache2-utils python php libapache2-mod-php

# create credential

# copy .htaccess file using echo to /var/www/html/.htaccess (read the readme.md for more information)
COPY files/.htaccess /var/www/html/.htaccess

COPY files/logging.php /var/www/html/logging.php
ENV REMOTE_USER="/var/www/html/logging.php"
RUN a2enmod rewrite
RUN touch /var/www/logins.log && chmod 777 /var/www/logins.log
# config apache
COPY files/apache2.conf /etc/apache2/apache2.conf

# start the service + wait for container
ENTRYPOINT service apache2 restart && tail