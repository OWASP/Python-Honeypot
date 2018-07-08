# OWASP Honeypot

[![Build Status](https://travis-ci.org/zdresearch/OWASPHoneyPot.svg?branch=master)](https://travis-ci.org/zdresearch/OWASPHoneyPot) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/5d4f23ebcfb0417e906ed29441f60050)](https://www.codacy.com/app/zdresearch/OWASP-Honeypot?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=zdresearch/OWASP-Honeypot&amp;utm_campaign=Badge_Grade)

##### ***WE ARE IN RESEARCH AND DEVELOP PHASE, EXPECT ERRORS!***
##### ***NO WARRANTY! USE WITH YOUR OWN RESPONSIBILITY!***
##### ***DO NOT USE IT ON THE SAME SERVER(S)/NETWORK WHICH YOU HAVING YOUR PRODUCT/INFORMATION/SENSIBLE DATA***


### Run
#### Install Dependencies
* Install `Docker` on your OS, check `docker info` if it's working and enable!
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

[+] OWASP Honeypot started ...
[+] loading modules ftp/weak_password, http/basic_auth_weak_password, ssh/weak_password
[+] creating image ohp_ftpserver
[+] image ohp_ftpserver created
[+] creating image ohp_httpserver
[+] image ohp_httpserver created
[+] creating image ohp_sshserver
[+] image ohp_sshserver created
[+] starting container ohp_ftpserver_weak_password
[+] container ohp_ftpserver_weak_password started
[+] starting container ohp_httpserver_basic_auth_weak_password
[+] container ohp_httpserver_basic_auth_weak_password started
[+] starting container ohp_sshserver_weak_password
[+] container ohp_sshserver_weak_password started
[+] all selected modules started: ftp/weak_password, http/basic_auth_weak_password, ssh/weak_password
[+] interrupted by user, please wait to stop the containers and remove the containers and images
[+] stopping container ohp_ftpserver_weak_password
[+] stopping container ohp_httpserver_basic_auth_weak_password
[+] stopping container ohp_sshserver_weak_password
[+] removing container ohp_ftpserver_weak_password
[+] removing container ohp_httpserver_basic_auth_weak_password
[+] removing container ohp_sshserver_weak_password
[+] removing image ohp_sshserver
[+] removing image ohp_httpserver
[+] removing image ohp_ftpserver
[+] finished.

C:\Users\Zombie\Documents\GitHub\OWASP-Honeypot>
```

* Please notice, everytime you run the honeypot, it will remove and update the virtual machine, so internet access required for the host!

We appreciate any contribution, ideas, feedback. feel free to contact us by creating an issue or send me email directly [ali.razmjoo@owasp.org](mailto:ali.razmjoo@owasp.org).
