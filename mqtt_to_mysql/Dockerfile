# Use an official python image as base
FROM python:3.9

# Set the working directory within the container
WORKDIR /app

# Copy requirements.txt and install the Python dependencies
COPY mqtt_to_mysql/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all Python files and configuration files to the working directoryctory
COPY mqtt_to_mysql /app/mqtt_to_mysql
COPY mqtt_to_mysql/main.py /app/main.py
COPY mqtt_to_mysql/mosquitto.conf /app/mosquitto.conf
COPY mqtt_to_mysql/sql_scripts /app/sql_scripts

# Set up PYTHONPATH so that Python can find the modules
ENV PYTHONPATH="/app:${PYTHONPATH}"

# Start main.py as entrypoint
CMD ["python", "/app/main.py"]
