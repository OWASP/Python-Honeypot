##
## Setup script for Ubuntu 18.04 Development system
##

pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install MongoDB
response=$(wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -)

if ["$response" == "OK"]; then
    continue
else
    sudo apt install gnupg
    wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -
fi

echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list
sudo apt-get update
sudo apt-get install -y mongodb-org
echo "mongodb-org hold" | sudo dpkg --set-selections
echo "mongodb-org-server hold" | sudo dpkg --set-selections
echo "mongodb-org-shell hold" | sudo dpkg --set-selections
echo "mongodb-org-mongos hold" | sudo dpkg --set-selections
echo "mongodb-org-tools hold" | sudo dpkg --set-selections

sudo systemctl daemon-reload
sudo systemctl start mongod
sudo systemctl enable mongod
sudo systemctl stop mongod
sudo systemctl restart mongod

# Install tshark

sudo apt install -y libgcrypt11-dev
sudo apt install bison flex
sudo apt install qttools5-dev-tools qttools5-dev libqt5svg5-dev qtmultimedia5-dev

# Install Optional Dependencies
sudo apt install libssh-dev asciidoctor libxml2-*
sudo apt install doxygen libpcap-dev gnutls* krb5-*
sudo apt install libsnappy1v5 libsnappy-dev libsnappy-java libsnappy-jni
sudo apt install libmaxminddb-dev libbrotli-dev libminizip-dev libspandsp-dev libcap-dev
sudo apt install libnghttp2-dev libzstd-dev xsltproc

wget https://www.wireshark.org/download/src/wireshark-3.2.2.tar.xz -O /tmp/wireshark-3.2.2.tar.xz
tar -xvf /tmp/wireshark-3.2.2.tar.xz --directory=/tmp/
cd /tmp/wireshark-3.2.2
sudo apt update && sudo apt dist-upgrade
sudo apt install cmake libglib2.0-dev libgcrypt20-dev flex yacc bison byacc \
  libpcap-dev qtbase5-dev libssh-dev libsystemd-dev qtmultimedia5-dev \
  libqt5svg5-dev qttools5-dev
cmake .
make
sudo make install