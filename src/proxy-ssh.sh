#!/usr/bin/env sh

cd proxy-vm/ || (>&2 echo "ERROR: The folder 'proxy-vm' does not exists."; exit)
vagrant ssh -- -t 'cd mitm/; python3 main.py'
