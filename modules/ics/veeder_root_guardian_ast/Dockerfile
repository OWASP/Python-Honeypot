# using phusion/baseimage as base image
FROM phusion/baseimage:0.9.19

# update and install apache + python
RUN apt-get update && apt-get install -y python

# copy gaspot service and config.ini file
COPY files/veeder_root_guardian_ast_service.py /root/veeder_root_guardian_ast_service.py
COPY files/config.py /root/config.py
COPY files/commands.py /root/commands.py

# run service
ENTRYPOINT cd /root; nohup python veeder_root_guardian_ast_service.py &> log.txt & tail