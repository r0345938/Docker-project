# Use an official Python image as base
FROM python:3.9

# Set the working directory within the container
WORKDIR /app

# copy requirements.txt and install the Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all Python files and configuration files to the working directory
COPY *.py /app/
COPY mosquitto.conf /app/
COPY sql_scripts /app/sql_scripts

# Run main.py as entrypoint
CMD ["python", "main.py"]
