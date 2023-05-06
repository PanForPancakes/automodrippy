sudo docker run -itd \
    --restart=always \
    --name dripcarbot \
    --mount type=bind,source=./user_data.json,target=/dripcarbot/user_data.json \
    --mount type=bind,source=./name_data.json,target=/dripcarbot/name_data.json \
    --mount type=bind,source=./frequency_data.json,target=/dripcarbot/frequency_data.json \
    dripcarbot:latest