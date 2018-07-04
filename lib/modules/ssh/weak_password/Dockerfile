FROM phusion/baseimage:0.9.19

RUN apt-get update && apt-get install -y openssh-* python

RUN echo {username}:{password} | /usr/sbin/chpasswd

RUN python -c "f=open(\"/etc/ssh/sshd_config\").read().replace(\"#Port 22\",\"Port 22\").replace(\"#PermitRootLogin yes\",\"PermitRootLogin yes\"); z = open(\"/etc/ssh/sshd_config\", \"w\");z.write(f); z.close(); print \"fixed sshd_config\""

RUN ssh-keygen -f id_rsa -t rsa -N '' && service ssh restart

EXPOSE {virtual_machine_port_number}