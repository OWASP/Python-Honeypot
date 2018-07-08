# using phusion/baseimage as base image
FROM phusion/baseimage:0.9.19

# update and install openssh + python
RUN apt-get update && apt-get install -y openssh-* python

# create credential
RUN echo {username}:{password} | /usr/sbin/chpasswd

# config ssh
RUN python -c "f=open(\"/etc/ssh/sshd_config\").read().replace(\"#Port 22\",\"Port 22\").replace(\"#PermitRootLogin yes\",\"PermitRootLogin yes\"); z = open(\"/etc/ssh/sshd_config\", \"w\");z.write(f); z.close(); print \"fixed sshd_config\""

# run ssh-keygen non-interactive
RUN ssh-keygen -f id_rsa -t rsa -N '' && service ssh restart

# start the service + wait for container
ENTRYPOINT service ssh restart && tail