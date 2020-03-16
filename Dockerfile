FROM ubuntu
MAINTAINER Chakshu Gupta
RUN apt update

RUN apt-get update && apt-get install -y \
    --no-install-suggests --no-install-recommends \
    add-apt-key \
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
    python-pip\
    python-setuptools \
    python2.7-dev \
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

RUN apt-get update
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get install -y mongodb-org
RUN echo "mongodb-org hold" | dpkg --set-selections
RUN echo "mongodb-org-server hold" | dpkg --set-selections
RUN echo "mongodb-org-shell hold" | dpkg --set-selections
RUN echo "mongodb-org-mongos hold" | dpkg --set-selections
RUN echo "mongodb-org-tools hold" | dpkg --set-selections

RUN wget https://www.wireshark.org/download/src/wireshark-3.2.2.tar.xz -O wireshark-3.2.2.tar.xz
RUN tar -xvf wireshark-3.2.2.tar.xz
RUN apt-get update && apt-get dist-upgrade
RUN cd wireshark-3.2.2 && cmake . && make && make install

# RUN systemctl daemon-reload
# RUN systemctl start mongod
# RUN systemctl enable mongod
# RUN systemctl stop mongod
# RUN systemctl restart mongod

RUN apt-get -yqq install krb5-user libpam-krb5

ARG CC=gcc-9
ARG CXX=g++-9

RUN git clone https://github.com/zdresearch/OWASP-Honeypot.git
RUN pip install wheel
RUN cd OWASP-Honeypot && pip install -r requirements.txt && pip install -r requirements-dev.txt
EXPOSE 5000
