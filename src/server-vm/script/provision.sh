#!/usr/bin/env sh

echo '#####   APT Update   #####'
sudo apt update

echo '#####   APT List Upgradable   #####'
sudo apt list --upgradable

echo '#####   APT Upgrade   #####'
sudo apt upgrade -yqq

echo '#####   APT Remove   #####'
sudo apt remove -yqq docker
sudo apt remove -yqq docker-compose
sudo apt remove -yqq docker-engine
sudo apt remove -yqq docker.io
sudo apt remove -yqq containerd
sudo apt remove -yqq runc
sudo apt remove -yqq docker-ce
sudo apt remove -yqq docker-ce-cli
sudo apt remove -yqq containerd.io

echo '#####   APT Install   #####'
sudo apt install -yqq \
   apt-transport-https \
   ca-certificates \
   curl \
   gnupg \
   lsb-release

echo '#####   Get GPG key   #####'
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo '#####   lsb_release   #####'
lsb_release -cs

echo '#####   Add Repository   #####'
sudo echo \
   "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

echo '#####   APT Update   #####'
sudo apt update

echo '#####   APT Install Docker   #####'
sudo apt install -yqq docker-ce docker-ce-cli containerd.io docker-compose

echo '#####   Add vagrant user to Docker group   #####'
sudo usermod -aG docker vagrant

echo '#####   Display Information   #####'
uname -a
docker --version
docker-compose --version

echo '#####   Docker Status   #####'
sudo systemctl status docker

echo '#####   Download PwnAdventure3   #####'
cd "${DOCKER_PATH}" || (>&2 echo "ERROR: The folder '${DOCKER_PATH}' does not exists."; exit)
sudo rm -fR client/
sudo rm -fR server/
sudo rm -fR postgres-data/
sudo rm -f pwn3.tar.gz*
wget -nv -q https://www.pwnadventure.com/pwn3.tar.gz

echo '#####   Extract PwnAdventure3   #####'
tar -xvf pwn3.tar.gz
rm -f pwn3.tar.gz*

echo '#####   Set up Docker Server   #####'
docker-compose build
