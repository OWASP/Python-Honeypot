# Use phusion/baseimage as base image. To make your builds
# reproducible, make sure you lock down to a specific version, not
# to `latest`! See
# https://github.com/phusion/baseimage-docker/blob/master/Changelog.md
# for a list of version numbers.
FROM phusion/baseimage:0.9.19

# Use baseimage-docker's init system.
CMD ["/sbin/my_init"]

RUN apt-get update && apt-get install -y vsftpd libpam-pwdfile apache2-utils
COPY etc/vsftpd.conf /etc/vsftpd.conf
COPY etc/vsftpd_user_conf/* /etc/vsftpd_user_conf/
COPY etc/pam.d/* /etc/pam.d/
COPY etc/init.d/vsftpd /etc/init.d/
RUN apt-get install -y ftp

RUN mkdir /etc/vsftpd && \
#    chmod +x /etc/service/vsftpd/run && \
    chmod +x /etc/init.d/vsftpd && \
    htpasswd -c -p -b /etc/vsftpd/ftpd.passwd admin $(openssl passwd -1 -noverify admin) && \
    useradd --home /home/vsftpd --gid nogroup -m --shell /bin/false vsftpd && \
    mkdir -p /var/www/html && \
    chown vsftpd:nogroup /var/www/html

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

EXPOSE 21 20 30000-30009
