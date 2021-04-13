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
# SELECT * FROM char_items;
# SELECT * FROM char_pickups;
# SELECT * FROM char_quests;
# SELECT * FROM char_slots;
# SELECT * FROM characters;
# SELECT * FROM info;
# SELECT * FROM names;
# SELECT * FROM team_state;
# SELECT * FROM teams;
# SELECT * FROM users;
# \q
# exit
# exit
# exit

# watch -n 0.1 "psql -d master -c 'SELECT * FROM char_items;'"
