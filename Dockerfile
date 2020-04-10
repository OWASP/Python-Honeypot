
FROM ubuntu:18.04

RUN apt-get -yqq update && apt-get -yqq upgrade && apt-get -yqq install \
    --no-install-suggests --no-install-recommends \
    apt-utils \
    asciidoctor \
    bison \
    build-essential \
    byacc \
    ca-certificates \
    cmake \
    dialog \
    doxygen \
    flex \
    git \
    gnupg \
    gnutls* \
    libbrotli-dev \
    libc++-9-dev \
    libcap-dev\
    libgcrypt20-dev \
    libglib2.0-dev \
    libmaxminddb-dev \
    libminizip-dev \
    libnghttp2-dev \
    libpcap-dev \
    libqt5svg5-dev \
    libsnappy-dev \
    libsnappy-java \
    libsnappy-jni \
    libsnappy1v5 \
    libspandsp-dev \
    libssh-dev \
    libsystemd-dev \
    libxml2-* \
    libzstd-dev \
    python3-pip\
    python3-wheel\
    python3.7 \
    python3.7-dev \
    qtbase5-dev \
    qtmultimedia5-dev \
    qttools5-dev-tools \
    qttools5-dev\
    wget \
    xsltproc

ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=DontWarn
RUN wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | apt-key add -

RUN echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-4.2.list

RUN apt-get -y update && apt-get -y upgrade
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get install -y \
    mongodb-org=4.2.3 \
    mongodb-org-server=4.2.3 \
    mongodb-org-shell=4.2.3 \
    mongodb-org-mongos=4.2.3 \
    mongodb-org-tools=4.2.3 \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /var/lib/mongodb \
    && mv /etc/mongod.conf /etc/mongod.conf.orig

RUN mkdir -p /data/db
RUN chown -R mongodb:mongodb /data/db

VOLUME ["/data/db"]

RUN wget https://www.wireshark.org/download/src/wireshark-3.2.2.tar.xz -O wireshark-3.2.2.tar.xz
RUN tar -xvf wireshark-3.2.2.tar.xz
RUN apt-get -y update && apt-get -y dist-upgrade
WORKDIR /wireshark-3.2.2
RUN cmake . && make && make install

# CMD ["systemctl","daemon-reload"]
# CMD ["systemctl", "start", "mongod"]
# CMD ["systemctl", "enable"," mongod"]
# CMD ["systemctl", "stop" ,"mongod"]
# CMD ["systemctl", "restart", "mongod"]

RUN apt-get -yqq install krb5-user libpam-krb5

ARG CC=gcc-9
ARG CXX=g++-9

ENV LC_CTYPE en_US.UTF-8
ENV LANG C.UTF-8
ENV LC_ALL en_US.UTF-8

RUN git clone https://github.com/zdresearch/OWASP-Honeypot.git /OWASP-Honeypot
WORKDIR /OWASP-Honeypot
RUN pip3 --no-cache-dir install --upgrade setuptools==46.1.3
RUN pip3 install -r requirements.txt
RUN pip3 install -r requirements-dev.txt
EXPOSE 5000
EXPOSE 27017

ENTRYPOINT ["python3", "ohp.py", "--start-api-server"]

CMD ["python3", "ohp.py"," -m all"]