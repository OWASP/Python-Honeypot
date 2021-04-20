# using phusion/baseimage as base image
FROM phusion/baseimage:master

# update and install apache + python
COPY files/requirements-apt-get.txt requirements-apt-get.txt
RUN apt-get update && xargs apt-get install -y < requirements-apt-get.txt

# copy gaspot service and config.ini file
COPY files/veeder_root_guardian_ast_service.py /root/veeder_root_guardian_ast_service.py

# run service
ENTRYPOINT cd /root; virtual_machine_port_number={virtual_machine_port_number} company_name_address="{company_name_address}" nohup python veeder_root_guardian_ast_service.py &> log.txt & tail
