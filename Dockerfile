FROM python:3.9-buster
WORKDIR /automodrippy

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY not_found.mp3 ./
COPY bot.py ./

COPY cars.txt ./
CMD [ "python", "./automodrippy.py" ]
