SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
cd $SCRIPT_DIR

docker build --tag annoto .  
docker run --rm -it  --mount type=bind,source=$SCRIPT_DIR,target=/home/a/annoto --network host --name annoto annoto
