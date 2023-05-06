FROM python:3.7-buster
WORKDIR /dripcarbot

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY cars.txt ./
COPY not_found.mp3 ./

COPY bot.py ./
CMD [ "python", "./bot.py" ]
