# using phusion/baseimage as base image
FROM ubuntu:20.04

# update and install openssh + python
COPY files/requirements-apt.txt files/requirements-py.txt ./

RUN apt-get update && xargs apt-get install -y < requirements-apt.txt

RUN pip3 install -r requirements-py.txt

COPY files/ssh_listener.py /root/ssh_listener.py
# create credential
RUN echo {username}:{password} | /usr/sbin/chpasswd
WORKDIR /root/
RUN mkdir -p logs

# start the service + wait for container
ENTRYPOINT  ssh-keygen -t rsa -N "" -f /root/.ssh/id_rsa >/dev/null && python3 /root/ssh_listener.py
