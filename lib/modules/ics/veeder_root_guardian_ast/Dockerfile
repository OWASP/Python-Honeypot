# using phusion/baseimage as base image
FROM phusion/baseimage:0.9.19

# update and install apache + python
RUN apt-get update && apt-get install -y python

# copy gaspot service and config.ini file
COPY files/veeder_root_guardian_ast_service.py /root/veeder_root_guardian_ast_service.py
COPY files/config.ini /root/config.ini

# run service
ENTRYPOINT cd /root; nohup python /root/veeder_root_guardian_ast_service(dot)py &> /root/log.txt & tail