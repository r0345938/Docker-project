Docker-Based IoT Data Pipeline with BMP180 Sensor Data Collection
Project Overview
This project is an end-to-end implementation of an Internet of Things (IoT) solution that collects environmental data using a BMP180 sensor connected to a Raspberry Pi. The collected data is streamed to a cloud-based architecture utilizing Azure services for data ingestion, processing, and storage. A Docker-based backup solution ensures data collection and visualization can function independently without cloud resources.
Key Project Features
1.	BMP180 Sensor Integration: Collection of temperature and pressure data using BMP180.
2.	Data Processing and Publishing: Azure IoT Hub is used for collecting the data and Azure Event Hub processes the incoming data stream.
3.	Database Storage: Data is stored in Azure Data Explorer, with a backup option using MySQL for local storage.
4.	Data Visualization: Grafana is used to visualize the data in a user-friendly way.
5.	Docker for Backup Implementation+Testing: Ensures that the system continues to function even when cloud components are unavailable.
6.	Testing: Rigorous unit, integration, and end-to-end testing to ensure the reliability and scalability of the system.
7.	Linux Environment on Raspberry Pi: The Raspberry Pi runs a lightweight Linux-based operating system that allows efficient resource utilization for IoT applications.
________________________________________
System Architecture
The architecture can be divided into different layers and services, each responsible for a critical aspect of the pipeline:
1. Data Collection
•	BMP180 Sensor: The BMP180 is an environmental sensor that collects both temperature and atmospheric pressure data. It uses the I2C protocol for communication with the Raspberry Pi Zero 2 W.
•	Raspberry Pi Zero 2 W:
o	The Raspberry Pi Zero 2 W runs a Linux-based operating system. This lightweight version of Linux is specifically tailored to provide a streamlined environment, allowing it to efficiently manage sensor data, networking, and containerized applications.
o	The Pi serves as the primary edge computing device that interacts directly with the BMP180 sensor.
o	Using Python libraries, the Pi reads data from the sensor, buffers the data to JSON files, and publishes it to the cloud using Azure IoT Hub.
o	The Linux environment provides important capabilities:
	Cron Jobs: Automated scheduling for reading and publishing data.
	Shell Scripting: For managing local data buffering and archiving.
	I2C Tools: For direct communication with the BMP180 sensor.
o	The collected sensor data is serialized into a JSON file with the format:
json
{
  "temperature": "<data>",
  "pressure": "<data>",
  "timestamp": "<time>"
}
o	This data is then used for further processing and transmission to the cloud or local systems.
2. Data Publishing and Processing
•	Azure IoT Hub: The Raspberry Pi publishes sensor data to Azure IoT Hub, which acts as a highly scalable and secure ingestion endpoint. Azure IoT Hub also manages device authentication and bidirectional communication.
•	Azure Event Hub: The IoT data received by IoT Hub is processed through Azure Event Hub. This is useful for decoupling data producers (like our Raspberry Pi) from data consumers (like databases) and helps in scaling.
3. Data Storage
•	Azure Data Explorer: The data from the Event Hub is ingested into Azure Data Explorer for long-term storage. Azure Data Explorer is optimized for querying massive amounts of data, making it suitable for the type of IoT data being collected.
•	MySQL Backup (in Docker):
o	The MySQL container acts as a backup if Azure services are not accessible.
o	It is hosted locally, and data is forwarded via an MQTT Broker, allowing continued operation even in offline scenarios.
o	Docker is used to containerize the database, ensuring easy portability and a consistent environment across different setups.
4. Data Visualization
•	Grafana:
o	Grafana is containerized using Docker and used to provide real-time data visualization.
o	Dashboards are created to display the temperature and pressure trends in a user-friendly manner.
o	MySQL serves as the data source for Grafana, and data is queried using SQL queries, presented in graphical formats.
________________________________________
Detailed Docker and Docker Compose Implementation
Why Docker?
Docker is used to provide containerized environments for several parts of the project. This helps achieve:
1.	Portability: Containers can be easily moved or replicated across different environments without worrying about dependencies.
2.	Scalability: Services can be scaled independently, allowing fine-tuned resource allocation.
3.	Isolation: The use of Docker allows running MySQL, Grafana, and MQTT Broker without interfering with the host system.
Docker Compose Configuration
The docker-compose.yml file is the core configuration file that defines and starts multiple containers at once.
Backup Implementation
The Dockerized implementation acts as a backup in case Azure services are unavailable. It replicates core functionality, including:
•	MQTT message brokering.
•	Data storage using MySQL.
•	Data visualization using Grafana.
This resilience ensures data continuity even during cloud outages.
________________________________________
Simulated Data (testdata.py)
Due to hardware limitations, I created a testdata.py script to simulate sensor data:
How testdata.py Works
•	Generates synthetic temperature and pressure data that resembles real sensor outputs.
•	The data is serialized as a JSON string and sent to the MQTT Broker.
•	The script runs at intervals, simulating the periodic publishing of data.
Publishing to MQTT Broker
•	The script connects to the MQTT Broker (mqtt-broker service in Docker) and publishes generated data to a specified topic.
•	This allowed for complete testing of the data pipeline and data visualization without requiring the physical BMP180 sensor.
________________________________________
Grafana Dashboard Provisioning
Grafana is used to visualize real-time data and give insights into temperature and pressure patterns.
•	The Grafana dashboard is provisioned automatically using a JSON configuration file (my_dashboard.json). This includes:
o	Temperature Graph: Shows temperature over time.
o	Pressure Graph: Visualizes pressure readings over time.
•	Data Source: MySQL is used as the primary data source, with SQL queries pulling timestamped sensor data into Grafana for plotting.
•	Grafana in Docker:
o	Port 3000 is used to access the Grafana UI.
o	The JSON dashboard is automatically loaded to make it easy to get started without manual configuration.
JSON Configuration
The my_dashboard.json file contains the full dashboard configuration, including panel layout, data queries, legends, and axis configurations. It also sets the timezone for the visualization to ensure all data points align correctly.
________________________________________
Testing Strategy
Testing is a critical aspect of this project to ensure all components function correctly both individually and together.
Testing Types
1.	Unit Tests:
o	Components Tested:
	Parsing MQTT messages.
	JSON serialization/deserialization.
	Individual functions for database operations.
o	Goal:
	Ensure the basic building blocks of the system work correctly.
2.	Integration Tests:
o	Components Tested Together:
	Raspberry Pi publishing data and the MQTT broker receiving it.
	MQTT broker forwarding data to MySQL.
o	Goal:
	Validate how different system components communicate.
	Ensure data flow from one service to another is seamless.
3.	End-to-End Tests:
o	Entire System:
	From data generation to visualization in Grafana.
	Uses synthetic data to simulate real-world scenarios.
o	Goal:
	Verify that all services work together without issues.
	Ensure that data integrity is maintained across all services.
Testing Pyramid
The testing pyramid has three layers, as:
1.	Unit Testing (Bottom Layer):
o	The largest layer represents unit tests that are easy to write and fast to execute.
o	These tests provide the foundation for a reliable system by validating small, isolated parts of the code.
2.	Integration Testing (Middle Layer):
o	Integration tests are fewer in number but more comprehensive.
o	They test how different parts of the system work together, ensuring there are no mismatches or failures during service communication.
3.	End-to-End Testing (Top Layer):
o	These tests are few but critical for validating the entire system in a production-like environment.
o	They simulate a complete workflow from data collection, data ingestion, database storage, to final visualization.
o	Given the high cost and complexity of these tests, they are performed less frequently but are essential for uncovering any issues that affect the entire pipeline.
Importance of Testing:
•	Early Bug Detection: Unit and integration testing help catch bugs early in the development cycle, reducing the cost and effort needed to fix issues.
•	Reliability: By performing end-to-end testing, we can ensure the final product is reliable and meets all requirements.
•	Scalability: Tests are designed to simulate different loads, helping in understanding how the system scales with increased data.
________________________________________
How to Run the Project
Prerequisites
•	Install Docker desktop and Docker Compose.
•	Ensure Python is installed to run the data simulation script.
Setup Instructions
1.	Clone the repository:
git clone https://github.com/r0345938/Docker-project.git
cd Docker-project
2.	Start Docker Containers:
o	Run the following command to start all services:
docker-compose up --build -d
o	This will set up the MySQL database, MQTT broker, and Grafana.
3.	View Dashboard in Grafana:
o	Open your browser and navigate to http://localhost:3000.
o	Use default credentials (admin/admin) to log in and view the "My Sensor Dashboard".


