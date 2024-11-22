MQTT Sensor Data Dashboard

Overview

This project is an end-to-end solution to collect, store, and visualize sensor data using MQTT, MySQL, Docker, and Grafana. The system collects temperature and pressure data from sensors via MQTT, stores it in a MySQL database, and visualizes it in real-time on a Grafana dashboard.

Project Architecture

MQTT Broker: Collects sensor data from various devices and forwards it to the MySQL database.

MySQL Database: Stores the sensor data. The table sensor_data contains columns for timestamp, temperature, and pressure.

Docker Compose: Used to set up and manage all the necessary containers (MQTT client, MySQL, Grafana).

Grafana: Visualizes the stored data in a clear dashboard with time series for temperature and pressure.

Project Objectives

This project is designed to:

Monitor and display sensor data in real-time.

Provide a scalable and repeatable infrastructure for storing and visualizing sensor information.

Utilize modern technologies like Docker and Grafana to provide an integrated monitoring solution.


Data Visualization

The Grafana dashboard displays temperature and pressure over time. The time series is identified by the timestamp column, and the values for temperature and pressure are displayed as line graphs.

Important Grafana Configuration Points

Datasource: The datasource in Grafana is configured to connect to the MySQL container (mysql-db:3306).

Dashboard Refresh: The dashboard is set to automatically refresh every 5 seconds, so you always see the most up-to-date data.

Troubleshooting

No Data in Grafana:

Check if the MySQL settings are correct in the mysql.yaml configuration file located in /grafana/provisioning/datasources/.

Ensure that the correct username and password are set for accessing the MySQL database.

Access Issues to MySQL:

If the error Access denied for user occurs, verify the credentials in the configuration file and make sure the MySQL user (mqtt_user) has the correct permissions.

Plugin Time Series Error in Grafana:

Check that the panel type is correctly set in the my_dashboard.json file.

File Structure

docker-compose.yml: Docker Compose configuration for setting up the MySQL, MQTT client, and Grafana services.

grafana/provisioning/datasources/mysql.yaml: Configuration file for the Grafana datasource to connect to MySQL.

grafana/dashboards/my_dashboard.json: Dashboard configuration for visualizing the sensor data.


Thank you for your interest in this project. Hopefully, this README helps you get started quickly!
