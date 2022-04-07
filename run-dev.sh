#!/bin/bash

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
cd $SCRIPT_DIR

trap 'docker container kill annoto' INT

docker build --tag annoto .  
echo $1
if [[ $1 == "--local-data-dir" ]]; then
    docker run --rm -it  --mount type=bind,source=$SCRIPT_DIR,target=/home/a/annoto --mount type=bind,source=$HOME/.annoto,target=/home/a/.annoto --network host --name annoto annoto
else
    docker run --rm -it  --mount type=bind,source=$SCRIPT_DIR,target=/home/a/annoto --network host --name annoto annoto
fi
