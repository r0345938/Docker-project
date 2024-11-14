# Gebruik een officiële Python image als basis
FROM python:3.9

# Stel de werkdirectory in binnen de container
WORKDIR /app

# Kopieer requirements.txt en installeer de Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopieer alle Python-bestanden en configuratiebestanden naar de werkdirectory
COPY *.py /app/
COPY mosquitto.conf /app/
COPY sql_scripts /app/sql_scripts

# Run de main.py als de entrypoint
CMD ["python", "main.py"]
