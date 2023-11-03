#!/bin/bash

docker run crashserver 
# wait a bit to let the container start
sleep 2
container_id=`docker ps -l -q`
echo "server container id: $container_id"
echo "to stop server run the following command: docker kill $container_id"