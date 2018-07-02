# OWASP Honeypot Project

### Features

* Emulator (DOCKER/LXC)
* Network Packet Analyzer
* Supporting Web/Network based Attacks
* Hacker Activity Monitor
* CLI/WebUI/API Available
* Secure Virtual Machine
* Automated Setup Process
* Live Reporting System
* Multi OS Agent

* to limit VM storage sizes change `/etc/init.d/docker` 
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