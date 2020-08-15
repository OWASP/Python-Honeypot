# using phusion/baseimage as base image
FROM phusion/baseimage:0.9.19

# update and install openssh + python
RUN apt-get update && apt-get install -y  python3

COPY files/smtpd_server/ /root/smtpd_server/
# start the service + wait for container

ENTRYPOINT cd /root/smtpd_server/ && python3 smtp_honeypot.py
