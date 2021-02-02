# using phusion/baseimage as base image
FROM phusion/baseimage:0.9.19

# use baseimage-docker's init system.
CMD ["/sbin/my_init"]

# update and install python3 and pip3
COPY files/requirements-apt.txt files/requirements-py.txt ./

RUN apt-get update && xargs apt-get install -y < requirements-apt.txt

RUN pip3 install -r requirements-py.txt

COPY files/ftp_sniffer.py /root/ftp_sniffer.py
COPY files/server.conf /root/server.conf

RUN echo {username}:{password} >> /root/users.conf
# install ftp (not necessary)
RUN apt-get install -y ftp

# start the service + wait for container
ENTRYPOINT python3 /root/ftp_sniffer.py
