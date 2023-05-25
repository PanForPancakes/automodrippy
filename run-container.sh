if [[ -z "$1" ]]; then
    echo "you haven't provided bot token!"
    exit
fi

docker stop automodrippy
docker rm automodrippy

docker run -itd \
    -e AUTOMODRIPPY_TOKEN=$1 \
    --restart=always \
    --name automodrippy \
    --mount type=bind,source=./user_data.json,target=/automodrippyv/user_data.json \
    --mount type=bind,source=./name_data.json,target=/automodrippy/name_data.json \
    --mount type=bind,source=./frequency_data.json,target=/automodrippy/frequency_data.json \
    automodrippy:latest