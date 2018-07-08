FROM phusion/baseimage:0.9.19

RUN apt-get update && apt-get install -y apache2 apache2-utils python

RUN htpasswd -b -c /var/www/html/.htpasswd {username} {password}

# copy .htaccess file using echo to /var/www/html/.htaccess
# AuthType Basic
# AuthName "Restricted Content"
# AuthUserFile /var/www/html/.htpasswd
# Require valid-user
RUN echo -e "\x41\x75\x74\x68\x54\x79\x70\x65\x20\x42\x61\x73\x69\x63\x0A\x41\x75\x74\x68\x4E\x61\x6D\x65\x20\x22\x52\x65\x73\x74\x72\x69\x63\x74\x65\x64\x20\x43\x6F\x6E\x74\x65\x6E\x74\x22\x0A\x41\x75\x74\x68\x55\x73\x65\x72\x46\x69\x6C\x65\x20\x2F\x76\x61\x72\x2F\x77\x77\x77\x2F\x68\x74\x6D\x6C\x2F\x2E\x68\x74\x70\x61\x73\x73\x77\x64\x0A\x52\x65\x71\x75\x69\x72\x65\x20\x76\x61\x6C\x69\x64\x2D\x75\x73\x65\x72" > /var/www/html/.htaccess

RUN python -c "f=open(\"/etc/apache2/apache2.conf\").read().replace(\"AllowOverride None\", \"AllowOverride All\");z=open(\"/etc/apache2/apache2.conf\", \"w\"); z.write(f); z.close(); print \"apache config modified...\""

EXPOSE {virtual_machine_port_number}

ENTRYPOINT service apache2 restart && tail