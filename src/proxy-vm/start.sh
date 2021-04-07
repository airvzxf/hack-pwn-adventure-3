#!/usr/bin/env sh

vagrant halt
vagrant up
vagrant ssh -- -t 'cd mitm/; python3 main.py'
