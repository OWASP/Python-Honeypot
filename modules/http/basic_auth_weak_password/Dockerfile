# using phusion/baseimage as base image
FROM phusion/baseimage:master

# update and install apache + python
COPY files/requirements-apt-get.txt requirements-apt-get.txt
RUN apt-get update && xargs apt-get install -y < requirements-apt-get.txt
# Remove possible evidence for honeypot
RUN rm -rf requirements-apt-get.txt

# create credential
RUN htpasswd -b -c /var/www/html/.htpasswd {username} {password}

# copy .htaccess file using echo to /var/www/html/.htaccess (read the readme.md for more information)
COPY files/.htaccess /var/www/html/.htaccess

# config apache
RUN sed -i 's/AllowOverride None/AllowOverride All/g' /etc/apache2/apache2.conf

# start the service + wait for container
ENTRYPOINT service apache2 restart && tail
