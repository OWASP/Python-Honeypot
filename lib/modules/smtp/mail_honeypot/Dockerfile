# using phusion/baseimage as base image
FROM phusion/baseimage:0.9.19

# update and install openssh + python
RUN apt-get update && apt-get install -y  python3

COPY files/smtp_honeypot.py /root/smtp_honeypot.py
# start the service + wait for container

CMD ["/root/smtp_honeypot.py"]
ENTRYPOINT ["python3"]
ENTRYPOINT cd /root/ && python3 smtp_honeypot.py
