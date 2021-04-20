# using phusion/baseimage as base image
FROM phusion/baseimage:master

# update and install openssh + python
COPY files/requirements-apt-get.txt requirements-apt-get.txt
RUN apt-get update && xargs apt-get install -y < requirements-apt-get.txt

COPY files/smtpd_server/ /root/smtpd_server/
# start the service + wait for container

ENTRYPOINT cd /root/smtpd_server/ && python3 smtp_honeypot.py
