FROM python:3.10-alpine
WORKDIR /automodrippy

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY sillydbmanager.py ./
COPY automodrippy.py ./

COPY cars.csv ./

CMD [ "python", "automodrippy.py" ]