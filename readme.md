# OWASP Honeypot

[![Build Status](https://travis-ci.org/zdresearch/OWASP-Honeypot.svg?branch=master)](https://travis-ci.org/zdresearch/OWASP-Honeypot) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/5d4f23ebcfb0417e906ed29441f60050)](https://www.codacy.com/app/zdresearch/OWASP-Honeypot?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=zdresearch/OWASP-Honeypot&amp;utm_campaign=Badge_Grade)

We appreciate any contribution, ideas, feedback. feel free to contact us by creating an issue or send me email directly [ali.razmjoo@owasp.org](mailto:ali.razmjoo@owasp.org).

##### ***WE ARE IN RESEARCH AND DEVELOP PHASE, EXPECT ERRORS!***
##### ***NO WARRANTY! USE WITH YOUR OWN RESPONSIBILITY!***
##### ***DO NOT USE IT ON THE SAME SERVER(S)/NETWORK WHICH YOU HAVING YOUR PRODUCT/INFORMATION/SENSIBLE DATA***

### Run
#### Install Dependencies
* Install `Docker` on your OS (Linux), check `docker info` if it's working and enable!
* Install `libpcap-dev`, `libnet-dev`, `tshark`, `pip install -r requirements.txt`
* Blocking virtual machines internet is not working on Windows (Didn't test on Mac!)
#### Start
* use `python ohp.py` to start the containers and default modules.

### Features

* Emulator (DOCKER/LXC)
* Multi OS Support
* Multi Python Version Support
* Secure Virtual Machine
* Automated Setup Process
* CLI ~~/WebUI/API~~ Available
* ~~Network Packet Analyzer~~
* ~~Supporting Web/Network based Attacks~~
* ~~Hacker Activity Monitor~~
* ~~Live Reporting System~~



* for now to limit VM storage sizes change `/etc/init.d/docker` 
```bash
log_begin_msg "Starting $DOCKER_DESC: $BASE"
start-stop-daemon --start --background \
	--no-close \
	--exec "$DOCKERD" \
	--pidfile "$DOCKER_SSD_PIDFILE" \
	--make-pidfile \
	-- \
		-p "$DOCKER_PIDFILE" \
		$DOCKER_OPTS \
			>> "$DOCKER_LOGFILE" 2>&1
log_end_msg $?
```

* to (add `--storage-opt dm.basesize=0.5G`)

```bash
log_begin_msg "Starting $DOCKER_DESC: $BASE"
start-stop-daemon --start --background \
	--no-close \
	--exec "$DOCKERD" --storage-opt dm.basesize=0.5G \
	--pidfile "$DOCKER_SSD_PIDFILE" \
	--make-pidfile \
	-- \
		-p "$DOCKER_PIDFILE" \
		$DOCKER_OPTS \
			>> "$DOCKER_LOGFILE" 2>&1
log_end_msg $?
```

* Running Example (I sent `ctrl + c` to close and remove honeypot service correctly!)

```
C:\Users\Zombie\Documents\GitHub\OWASP-Honeypot>python ohp.py

      ______          __      _____ _____
     / __ \ \        / /\    / ____|  __ \
    | |  | \ \  /\  / /  \  | (___ | |__) |
    | |  | |\ \/  \/ / /\ \  \___ \|  ___/
    | |__| | \  /\  / ____ \ ____) | |
     \____/   \/  \/_/    \_\_____/|_|
                      _    _                        _____      _
                     | |  | |                      |  __ \    | |
                     | |__| | ___  _ __   ___ _   _| |__) |__ | |_
                     |  __  |/ _ \| "_ \ / _ \ | | |  ___/ _ \| __|
                     | |  | | (_) | | | |  __/ |_| | |  | (_) | |_
                     |_|  |_|\___/|_| |_|\___|\__, |_|   \___/ \__|
                                               __/ |
                                              |___/

[+] [2018-07-09 23:56:06] OWASP Honeypot started ...
[+] [2018-07-09 23:56:06] loading modules ftp/weak_password, http/basic_auth_weak_password, ssh/weak_password
[+] [2018-07-09 23:56:06] creating image ohp_ftpserver
[+] [2018-07-09 23:56:35] image ohp_ftpserver created
[+] [2018-07-09 23:56:35] creating image ohp_httpserver
[+] [2018-07-09 23:57:00] image ohp_httpserver created
[+] [2018-07-09 23:57:00] creating image ohp_sshserver
[+] [2018-07-09 23:57:17] image ohp_sshserver created
[+] [2018-07-09 23:57:17] creating ohp_internet network
[+] [2018-07-09 23:57:17] ohp_internet network created subnet:172.19.0.0/16 gateway:172.19.0.1
[+] [2018-07-09 23:57:17] creating ohp_no_internet network
[+] [2018-07-09 23:57:18] ohp_no_internet network created subnet:172.20.0.0/16 gateway:172.20.0.1
[+] [2018-07-09 23:57:18] container ohp_ftpserver_weak_password started, forwarding 0.0.0.0:21 to 72.20.0.:21
[+] [2018-07-09 23:57:18] container ohp_httpserver_basic_auth_weak_password started, forwarding 0.0.0.0:80 to 72.20.0.:80
[+] [2018-07-09 23:57:19] container ohp_sshserver_weak_password started, forwarding 0.0.0.0:22 to 72.19.0.:22
[+] [2018-07-09 23:57:19] all selected modules started: ftp/weak_password, http/basic_auth_weak_password, ssh/weak_password
[+] [2018-07-09 23:57:29] interrupted by user, please wait to stop the containers and remove the containers and images
[+] [2018-07-09 23:57:39] stopping container ohp_httpserver_basic_auth_weak_password
[+] [2018-07-09 23:57:49] stopping container ohp_sshserver_weak_password
[+] [2018-07-09 23:57:49] removing container ohp_ftpserver_weak_password
[+] [2018-07-09 23:57:49] removing container ohp_httpserver_basic_auth_weak_password
[+] [2018-07-09 23:57:49] removing container ohp_sshserver_weak_password
[+] [2018-07-09 23:57:49] removing image ohp_sshserver
[+] [2018-07-09 23:57:49] removing image ohp_httpserver
[+] [2018-07-09 23:57:49] removing image ohp_ftpserver
[+] [2018-07-09 23:57:49] finished.

C:\Users\Zombie\Documents\GitHub\OWASP-Honeypot>
```

* Please notice, everytime you run the honeypot, it will remove and update the virtual machine, so internet access required for the host!

#### API Actions

![image_2018-07-17_01-48-26](https://user-images.githubusercontent.com/7676267/42784742-63f95a2e-8965-11e8-8d64-435f6182dcf2.png)

```python
action: "http://127.0.0.1:5000/api/events/count_all_events" 
time: 0.010449
response: count_all_events":2045253}

action: "http://127.0.0.1:5000/api/events/count_ohp_events" 
time: 0.010053
response: count_ohp_events":948302}

action: "http://127.0.0.1:5000/api/events/count_network_events" 
time: 0.009567
response: count_network_events":1096951}

action: "http://127.0.0.1:5000/api/events/count_network_events_by_date" 
time: 0.009215
response: count_network_events_by_date":0,"date":null}

action: "http://127.0.0.1:5000/api/events/count_honeypot_events_by_date" 
time: 0.008931
response: count_honeypot_events_by_date":0,"date":null}

action: "http://127.0.0.1:5000/api/events/count_all_events_by_date" 
time: 0.009389
response: count_all_events_by_date":0,"date":null}

action: "http://127.0.0.1:5000/api/events/top_ten_ips_in_honeypot_events" 
time: 3.239441 
response: [{"_id":"192.168.1.6","count":805},{"_id":"192.168.1.3","count":795},{"_id":"192.168.1.9","count":779},{"_id":"192.168.1.5","count":747},{"_id":"192.168.1.2","count":693},{"_id":"192.168.1.7","count":687},{"_id":"192.168.1.4","count":677},{"_id":"192.168.1.8","count":642},{"_id":"192.168.1.77","count":642},{"_id":"192.168.1.82","count":636}]

action: "http://127.0.0.1:5000/api/events/top_ten_ips_in_network_events" 
time: 3.503781 
response:  [{"_id":"192.168.1.5","count":1423},{"_id":"192.168.1.7","count":1369},{"_id":"192.168.1.4","count":1364},{"_id":"192.168.1.6","count":1313},{"_id":"192.168.1.9","count":1307},{"_id":"192.168.1.3","count":1303},{"_id":"192.168.1.2","count":1284},{"_id":"192.168.1.8","count":1276},{"_id":"192.168.1.66","count":1261},{"_id":"192.168.1.85","count":1242}]

action: "http://127.0.0.1:5000/api/events/top_ten_ports_in_honeypot_events" 
time: 1.747325 
response:  [{"_id":80,"count":1140},{"_id":21,"count":71},{"_id":56017,"count":32},{"_id":64712,"count":31},{"_id":43518,"count":31},{"_id":39985,"count":31},{"_id":3518,"count":31},{"_id":1061,"count":31},{"_id":50774,"count":30},{"_id":43363,"count":30}]

action: "http://127.0.0.1:5000/api/events/top_ten_ports_in_network_events" 
time: 1.957787 
response:  [{"_id":80,"count":462},{"_id":443,"count":444},{"_id":22,"count":48},{"_id":45952,"count":35},{"_id":50106,"count":34},{"_id":24622,"count":34},{"_id":61266,"count":33},{"_id":59598,"count":33},{"_id":57242,"count":33},{"_id":50799,"count":33}]
```