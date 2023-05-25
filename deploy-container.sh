# get token

if [ ! -f TOKEN ]; then
    echo "TOKEN file doesn't exist."
    echo "Abort."
    exit 1
fi

automodrippy_token="cat TOKEN"

if [[ -z "$automodrippy_token" ]]; then
    echo "No bot token in TOKEN file"
    echo "You can do something like this:"
    echo "echo \"<your_token_here> >\" > TOKEN"
    echo "...and then rerun this script again."
    echo "Abort."
    exit 1

# find out what builder we are using [docker > podman]

docker --version > /dev/null
if [ $? -eq 0 ]; then
    builder=docker
fi

podman --version > /dev/null
if [ $? -eq 0 ]; then
    builder=podman
fi

if [[ -z "$builder" ]]; then
    echo "Neither usable docker or podman are found."
    echo "Abort."
    exit 1
fi

# build new container

$builder build --tag automodrippy .

# stop and remove old container if exist

$builder stop --ignore automodrippy
$builder rm --ignore automodrippy

# make sure data dir exists

mkdir -p data

# start new container

$builder run -itd \
    -e AUTOMODRIPPY_TOKEN=$automodrippy_token \
    --restart=always \
    --name automodrippy \
    --mount type=bind,source=./data,target=/automodrippy \
    automodrippy:latest