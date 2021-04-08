#!/usr/bin/env sh

cd ./server-vm/ || (>&2 echo "ERROR: The folder 'server-vm' does not exists."; exit)
./backup-database.sh
