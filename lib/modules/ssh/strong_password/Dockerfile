# using phusion/baseimage as base image
FROM phusion/baseimage:0.9.19

# update and install openssh + python
RUN apt-get update && apt-get install -y python3.5 python3-pip python3-dev python-pip libssl-dev libffi-dev

RUN pip3 install paramiko
RUN pip3 install datetime

COPY files/ssh_listener.py /root/ssh_listener.py
# create credential
RUN echo {username}:{password} | /usr/sbin/chpasswd
WORKDIR /root/
RUN mkdir -p logs

# start the service + wait for container
ENTRYPOINT  ssh-keygen -t rsa -N "" -f /root/.ssh/id_rsa >/dev/null && python3 /root/ssh_listener.py
