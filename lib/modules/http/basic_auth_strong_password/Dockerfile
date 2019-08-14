# using phusion/baseimage as base image
FROM phusion/baseimage:0.9.19

# update and install apache + python

RUN apt-get update && apt-get install -y apache2 apache2-utils python

# create credential
RUN htpasswd -b -c /var/www/html/.htpasswd {username} {password}

# copy .htaccess file using echo to /var/www/html/.htaccess (read the readme.md for more information)
COPY files/.htaccess /var/www/html/.htaccess

# config apache
COPY files/apache2.conf /etc/apache2/apache2.conf

# start the service + wait for container
ENTRYPOINT service apache2 restart && tail