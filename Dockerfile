FROM python:3.10-alpine
WORKDIR /automodrippy

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY not_found.mp3 ./
COPY automodrippy.py ./

COPY cool_things.py ./

COPY cars.txt ./
CMD [ "python", "automodrippy.py" ]