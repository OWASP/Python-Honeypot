### Docker VSFTPD

Simple ftp server with docker

### usage

```docker build . -t ftpserver
docker run -d ftpserver
docker exec -it 7f121dcaecca /bin/bash -c "service vsftpd start"```

* Ref: https://github.com/lrkwz/docker-vsftp