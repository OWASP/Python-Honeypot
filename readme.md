# OWASP Honeypot

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
* CLI~~/WebUI/API~~ Available
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

We appreciate any contribution, ideas, feedback. feel free to contact us by creating an issue or send me email directly [ali.razmjoo@owasp.org](mailto:ali.razmjoo@owasp.org).