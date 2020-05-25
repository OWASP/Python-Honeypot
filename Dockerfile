FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -yqq update && apt-get -yqq upgrade && apt-get -yqq install \
    --no-install-suggests --no-install-recommends \
    apt-transport-https\
    apt-utils \
    asciidoctor \
    bison \
    build-essential \
    byacc \
    ca-certificates \
    cmake \
    curl\
    dialog \
    doxygen \
    flex \
    git \
    gnupg \
    gnupg2\
    gnutls* \
    krb5-user \
    libbrotli-dev \
    libc++-9-dev \
    libcap-dev\
    libgcrypt20-dev \
    libglib2.0-dev \
    libmaxminddb-dev \
    libminizip-dev \
    libnghttp2-dev \
    libpam-krb5 \
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
    mongodb \
    mongodb-clients \
    mongo-tools \
    python3-pip\
    python3-wheel\
    python3.8 \
    python3.8-dev \
    qtbase5-dev \
    qtmultimedia5-dev \
    qttools5-dev-tools \
    qttools5-dev\
    software-properties-common\
    tshark \
    wget \
    xsltproc

RUN git clone https://github.com/zdresearch/OWASP-Honeypot.git /OWASP-Honeypot
WORKDIR /OWASP-Honeypot

RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - &&\
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable" &&\
    apt-get -y update && apt-get install -y docker-ce
    
RUN pip3 --no-cache-dir install --upgrade setuptools==46.1.3
RUN pip3 install -r requirements.txt
RUN pip3 install -r requirements-dev.txt

RUN service docker start

CMD [ "python3","-m", "pytest", "-rpP" ]