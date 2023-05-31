# make sure data folder exists

mkdir -p automodrippy_data

# copy cars.csv from repository if it doesn't exist in data folder

if [ ! -f automodrippy_data/cars.csv ]; then
    echo "cars.csv file doesn't exist -->"
    echo "--> copying one from repository"
    cp cars.csv automodrippy_data/
fi

# get token

if [ ! -f automodrippy_data/TOKEN ]; then
    echo "No bot token in TOKEN file"
    echo "You can do something like this:"
    echo "echo \"<your_token_here>\" > automodrippy_data/TOKEN"
    echo "...and then rerun this script again."
    echo "Abort."
    exit 1
fi

automodrippy_token=`cat automodrippy_data/TOKEN`

if [[ -z "$automodrippy_token" ]]; then
    echo "No bot token in TOKEN file"
    echo "You can do something like this:"
    echo "echo \"<your_token_here>\" > automodrippy_data/TOKEN"
    echo "...and then rerun this script again."
    echo "Abort."
    exit 1
fi

# find out what builder we are using [docker > podman]

if [ -x "$(command -v docker --version)" ]; then
    builder=docker
elif [ -x "$(command -v podman --version)" ]; then
    builder=podman
else
    echo "Neither usable docker or podman are found."
    echo "Abort."
    exit 1
fi

# build new container

$builder build --tag automodrippy .

# stop and remove old container if exist

$builder stop --time 1 --ignore automodrippy
$builder rm --ignore automodrippy

# start new container

$builder run -itd \
    -e AUTOMODRIPPY_TOKEN="$automodrippy_token" \
    --restart=always \
    --name automodrippy \
    --mount type=bind,source=./automodrippy_data,target=/automodrippy/automodrippy_data \
    localhost/automodrippy:latest