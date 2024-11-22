# Gebruik een officiële Python image als basis
FROM python:3.9

# Stel de werkdirectory binnen de container in
WORKDIR /app

# Kopieer requirements.txt en installeer de Python afhankelijkheden
COPY mqtt_to_mysql/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopieer alle Python bestanden en configuratiebestanden naar de werkdirectory
COPY mqtt_to_mysql /app/mqtt_to_mysql
COPY mqtt_to_mysql/main.py /app/main.py
COPY mqtt_to_mysql/mosquitto.conf /app/mosquitto.conf
COPY mqtt_to_mysql/sql_scripts /app/sql_scripts

# Stel PYTHONPATH in zodat Python de modules kan vinden
ENV PYTHONPATH="/app:${PYTHONPATH}"

# Start main.py als entrypoint
CMD ["python", "/app/main.py"]
