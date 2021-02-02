# using phusion/baseimage as base image
FROM phusion/baseimage:0.9.19

# update and install openssh + python
COPY files/requirements-apt.txt requirements-apt.txt
RUN apt-get update && xargs apt-get install -y < requirements-apt.txt

COPY files/smtpd_server/ /root/smtpd_server/
# start the service + wait for container

ENTRYPOINT cd /root/smtpd_server/ && python3 smtp_honeypot.py
