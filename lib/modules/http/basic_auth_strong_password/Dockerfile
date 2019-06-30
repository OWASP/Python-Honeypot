# using phusion/baseimage as base image
FROM phusion/baseimage:0.9.19

# update and install apache + python
RUN apt-get update && apt-get install -y python3.5 python3-pip python3-dev


RUN pip3 install datetime

COPY files/http_sniffer.py /root/http_sniffer.py
# create credential

# copy .htaccess file using echo to /var/www/html/.htaccess (read the readme.md for more information)
COPY files/.htaccess /var/www/html/.htaccess

WORKDIR /root/
RUN mkdir -p logs
# start the service + wait for container
ENTRYPOINT python3 /root/http_sniffer.py