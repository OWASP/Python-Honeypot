# using phusion/baseimage as base image
FROM phusion/baseimage:0.9.19

# update and install apache + python
RUN apt-get update && apt-get install -y python3.5

# copy gaspot service and config.ini file
COPY files/veeder_root_guardian_ast_service.py /root/veeder_root_guardian_ast_service.py

# run service
ENTRYPOINT cd /root; virtual_machine_port_number={virtual_machine_port_number} company_name_address="{company_name_address}" nohup python veeder_root_guardian_ast_service.py &> log.txt & tail