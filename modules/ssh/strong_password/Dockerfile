# using phusion/baseimage as base image
FROM ubuntu:20.04

# update and install openssh + python
COPY files/requirements-apt-get.txt files/requirements-pip3.txt ./

RUN apt-get update && xargs apt-get install -y < requirements-apt-get.txt

RUN pip3 install -r requirements-pip3.txt

COPY files/ssh_listener.py /root/ssh_listener.py
# create credential
RUN echo {username}:{password} | /usr/sbin/chpasswd
WORKDIR /root/
RUN mkdir -p logs

# start the service + wait for container
ENTRYPOINT  ssh-keygen -t rsa -N "" -f /root/.ssh/id_rsa >/dev/null && python3 /root/ssh_listener.py
