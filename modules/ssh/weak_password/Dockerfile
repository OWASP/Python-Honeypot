# using phusion/baseimage as base image
FROM phusion/baseimage:master

# update and install openssh + python
COPY files/requirements-apt-get.txt requirements-apt-get.txt
RUN apt-get update && xargs apt-get install -y < requirements-apt-get.txt
# Remove possible evidence for honeypot
RUN rm -rf requirements-apt-get.txt

# create credential
RUN echo {username}:{password} | /usr/sbin/chpasswd

# config ssh
RUN sed -i 's/#Port 22/Port 22/g' /etc/ssh/sshd_config
RUN sed -i 's/#PermitRootLogin yes/PermitRootLogin yes/g' /etc/ssh/sshd_config

# run ssh-keygen non-interactive
RUN ssh-keygen -k -f id_rsa -t rsa -N '' -f /root/.ssh/id_rsa >/dev/null && ssh-keygen -A && service ssh restart

# start the service + wait for container
ENTRYPOINT service ssh restart && tail
