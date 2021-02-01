# using phusion/baseimage as base image
FROM ubuntu:20.04

# update and install openssh + python
RUN apt-get update && apt-get install -y python3.5 python3-pip \
    libffi-dev=3.3-4 python3-dev=3.8.2-0ubuntu2 libssl-dev=1.1.1f-1ubuntu2.1 \
    openssh-client=1:8.2p1-4ubuntu0.1

RUN pip3 install paramiko==2.7.2
RUN pip3 install datetime==4.3

COPY files/ssh_listener.py /root/ssh_listener.py
# create credential
RUN echo {username}:{password} | /usr/sbin/chpasswd
WORKDIR /root/
RUN mkdir -p logs

# start the service + wait for container
ENTRYPOINT  ssh-keygen -t rsa -N "" -f /root/.ssh/id_rsa >/dev/null && python3 /root/ssh_listener.py
