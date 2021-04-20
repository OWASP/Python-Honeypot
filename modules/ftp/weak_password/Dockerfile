# using phusion/baseimage as base image
FROM phusion/baseimage:master

# use baseimage-docker's init system.
CMD ["/sbin/my_init"]

# update and install vsftpd + libs
COPY files/requirements-apt-get.txt requirements-apt-get.txt
RUN apt-get update && xargs apt-get install -y < requirements-apt-get.txt
# Remove possible evidence for honeypot
RUN rm -rf requirements-apt-get.txt

# copy vsftpd.conf to /etc/vsftpd.conf
COPY files/vsftpd.conf /etc/vsftpd.conf

# create user config
RUN mkdir -p /etc/vsftpd_user_conf && echo "local_root=/var/www/html" > /etc/vsftpd_user_conf/{username}

RUN mkdir -p /etc/pam.d/
RUN echo "auth required pam_pwdfile.so pwdfile /etc/vsftpd/ftpd.passwd" > /etc/pam.d/vsftpd
RUN echo "account required pam_permit.so" >> /etc/pam.d/vsftpd

# create /etc/init.d/vsftpd
COPY files/vsftpd.sh /etc/init.d/vsftpd
# install ftp (not necessary)
RUN apt-get install -y ftp

# configuration
RUN mkdir /etc/vsftpd && \
#    chmod +x /etc/service/vsftpd/run && \
    chmod +x /etc/init.d/vsftpd && \
    htpasswd -c -p -b /etc/vsftpd/ftpd.passwd {username} $(openssl passwd -1 -noverify {password}) && \
    useradd --home /home/vsftpd --gid nogroup -m --shell /bin/false vsftpd && \
    mkdir -p /var/www/html && \
    chown vsftpd:nogroup /var/www/html

# start the service + wait for container
ENTRYPOINT service vsftpd restart & chmod +x /root/history_append.sh & tail
