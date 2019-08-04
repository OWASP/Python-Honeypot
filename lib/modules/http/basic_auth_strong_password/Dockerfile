# using phusion/baseimage as base image
FROM phusion/baseimage:0.9.19

# update and install apache + python

RUN apt-get update && apt-get install -y apache2 apache2-utils python php libapache2-mod-php

RUN pip3 install datetime

COPY files/http_sniffer.py /root/http_sniffer.py
# create credential

# copy .htaccess file using echo to /var/www/html/.htaccess (read the readme.md for more information)
COPY files/.htaccess /var/www/html/.htaccess

COPY files/logging.php /var/www/html/logging.php
ENV REMOTE_USER="/var/www/html/logging.php"
RUN a2enmod rewrite
RUN touch /var/www/logins.log && chmod 777 /var/www/logins.log
# config apache
RUN python -c "f=open(\"/etc/apache2/apache2.conf\").read().replace(\"AllowOverride None\", \"AllowOverride All\");z=open(\"/etc/apache2/apache2.conf\", \"w\"); z.write(f); z.close(); print \"apache config modified...\""

# start the service + wait for container
ENTRYPOINT service apache2 restart && tail