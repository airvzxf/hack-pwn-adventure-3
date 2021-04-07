#!/usr/bin/env sh

echo '#####   Start PwnAdventure3   #####'
cd "${DOCKER_PATH}" || (>&2 echo "ERROR: The folder '${DOCKER_PATH}' does not exists."; exit)
docker-compose up -d

echo '#####   Starting...   #####'
echo 'It could take less than one minute.'
echo 'It will not show any success message.'
echo 'You need to make several attempts in your game to start playing.'
