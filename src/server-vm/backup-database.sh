#!/usr/bin/env sh

vagrant ssh -- -tt 'docker exec -it docker_master_1 ' \
  '/bin/bash -c "' \
  'rm -f /opt/pwn3/postgres-data/data.sql;' \
  'sudo -u pwn3 pg_dump master > /opt/pwn3/postgres-data/data.sql;' \
  '"'

# vagrant ssh
# # Vagrant
# docker exec -it docker_master_1 /bin/bash
# # Docker
# sudo -i -u pwn3
# psql master
# \pset pager off
# \l+
# \c master
# \dt+
# select * from char_items;
# select * from char_pickups;
# select * from char_quests;
# select * from char_slots;
# select * from characters;
# select * from info;
# select * from names;
# select * from team_state;
# select * from teams;
# select * from users;
# \q
# exit
# exit
# exit
