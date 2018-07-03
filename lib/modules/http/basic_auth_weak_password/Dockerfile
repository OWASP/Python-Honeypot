FROM phusion/baseimage:0.9.19

RUN apt-get update && apt-get install -y apache2 apache2-utils python

RUN htpasswd -b -c /var/www/html/.htpasswd admin 123456

COPY .htaccess /var/www/html/.htaccess

RUN chown  www-data:www-data * .ht*

RUN python -c "f=open(\"/etc/apache2/apache2.conf\").read().replace(\"AllowOverride None\", \"AllowOverride All\");z=open(\"/etc/apache2/apache2.conf\", \"w\"); z.write(f); z.close(); print \"apache config modified...\""

RUN service apache2 restart

EXPOSE 80