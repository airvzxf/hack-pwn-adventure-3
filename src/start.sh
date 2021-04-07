#!/usr/bin/env sh

cd ./server-vm/ || (>&2 echo "ERROR: The folder 'server-vm' does not exists."; exit)
./start.sh

cd ../proxy-vm/ || (>&2 echo "ERROR: The folder 'proxy-vm' does not exists."; exit)
./start.sh
