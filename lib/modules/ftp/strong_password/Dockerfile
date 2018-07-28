# using phusion/baseimage as base image
FROM phusion/baseimage:0.9.19

# use baseimage-docker's init system.
CMD ["/sbin/my_init"]

# update and install vsftpd + libs
RUN apt-get update && apt-get install -y vsftpd libpam-pwdfile apache2-utils

# copy vsftpd.conf to /etc/vsftpd.conf using echo (read the readme.md for more information)
RUN {write_file_by_to_docker_image(vsftpd(dot)conf,/etc/vsftpd(dot)conf)}

# create user config
RUN mkdir -p /etc/vsftpd_user_conf && echo "local_root=/var/www/html" > /etc/vsftpd_user_conf/{username}

RUN mkdir -p /etc/pam.d/ && echo -e "auth required pam_pwdfile.so pwdfile /etc/vsftpd/ftpd.passwd\x0aaccount required pam_permit.so" > /etc/pam.d/vsftpd

# create /etc/init.d/vsftpd using echo (read the readme.md for more information)
RUN {write_file_by_to_docker_image(vsftpd(dot)sh,/etc/init(dot)d/vsftpd)}

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
ENTRYPOINT service vsftpd restart & tail
