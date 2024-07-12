# SmartGreenhouse

## About the Project

SmartGreenhouse aims to create an intelligent greenhouse that captures internal and external environmental conditions using a variety of sensors. The collected data is stored in a database for later analysis. Additionally, the project utilizes collected rainwater to ensure an independent water supply. A central component of the greenhouse is the FarmBot, which fully autonomously tends to the plants from sowing to harvest.

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [Authors](#authors)
- [License](#license)
- [Diagrams](#diagrams)

## Features

- **Data Collection**: Comprehensive monitoring of environmental conditions both inside and outside the greenhouse.
- **Water Recycling**: Independence from external water supply through the use of rainwater.
- **Autonomous Plant Care**: Use of a FarmBot for fully automatic care of the plants.

## Technologies

- **Backend**: Flask (Python)
- **Database**: SQLAlchemy
- **Automation**: Integration of FarmBot

## Installation

1. **Clone the Repository**:
   ```
   git clone https://github.com/ETCE-LAB/ETCE-Farmbot-Smart-Greenhouse.git
   cd ETCE-Farmbot-Smart-Greenhouse
   ```

2. **Create and Activate a Virtual Environment**:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Required Dependencies**:
   ```
   pip install -r requirements.txt
   ```

## Usage

Start the backend with:

```
python main.py
```

The Flask endpoints can be accessed via the provided Swagger UI at `http://localhost:5000/swagger`.

## API Endpoints

### FarmBot Management
- **Description**: Endpoints for controlling and monitoring the FarmBot.
- **Endpoints**:
  - **GET `/farmbot/move/<float:x>/<float:y>/<float:z>`**: Moves the FarmBot to the specified coordinates.
  - **GET `/farmbot/action/waterField`**: Activates the irrigation function of the FarmBot.
  - **GET `/farmbot/measure/measureSoilMoisture`**: Measures soil moisture.

### Weather Station
- **Description**: Endpoints for capturing and processing weather station data.
- **Endpoints**:
  - **GET `/station/data/<date>`**: Displays weather data for a specific date.
    - **Response**:
      ```json
      {
        "id": 101,
        "measurement_value": 22.5,
        "measurement_type": "Temperature",
        "received_at": "2024-07-12T15:30:00Z"
      }
      ```
  - **GET `/station/data/range/<start_date>/<end_date>`**: Retrieves weather data for a specified date range.
    - **Response**:
      ```json
      [
        {
          "id": 102,
          "measurement_value": 21.5,
          "measurement_type": "Temperature",
          "received_at": "2024-07-11T15:30:00Z"
        },
        {
          "id": 103,
          "measurement_value": 23.0,
          "measurement_type": "Temperature",
          "received_at": "2024-07-12T15:30:00Z"
        }
      ]
      ```
  - **POST `/station/data`**: Creates new weather station data. **For developer debugging only; must be removed in production release.**

### Weather Forecast
- **Description**: Endpoints for querying weather forecasts.
- **Endpoints**:
  - **GET `/forecast/<date>`**: Retrieves weather forecast data for a specific date.
    - **Response**:
      ```json
      {
        "id": 202,
        "date": "2024-07-13",
        "max_temperature": 25.0,
        "min_temperature": 15.0,
        "sunshine_duration_minutes": 320,
        "precipitation_mm": 5.0
      }
      ```
  - **GET `/forecast/range/<start_date>/<end_date>`**: Retrieves weather forecast data for a specified date range.
    - **Response**:
      ```json
      [
        {
          "id": 203,
          "date": "2024-07-14",
          "max_temperature": 24.0,
          "min_temperature": 14.0,
          "sunshine_duration_minutes": 300,
          "precipitation_mm": 2.0
        },
        {
          "id": 204,
          "date": "2024-07-15",
          "max_temperature": 26.0,
          "min_temperature": 16.0,
          "sunshine_duration_minutes": 340,
          "precipitation_mm": 8.0
        }
      ]
      ```
  - **POST `/forecast`**: Creates new forecast data. **For developer debugging only; must be removed in production release.**

### Water Management
- **Description**: Endpoints for managing water consumption and storage.
- **Endpoints**:
  - **GET `/water/volume/<date>`**: Displays water volume on a specific date.
    - **Response**:
      ```json
      {
        "id": 303,
        "date": "2024-07-12",
        "volume": 1500.0
      }
      ```
  - **GET `/water/volume/range/<start_date>/<end_date>`**: Displays water volume data for a specified date range.
    - **Response**:
      ```json
      [
        {
          "id": 304,
          "date": "2024-07-10",
          "volume": 1480.0
        },
        {
          "id": 305,
          "date": "2024-07-11",
          "volume": 1495.0
        }
      ]
      ```
  - **POST `/water/volume`**: Creates new water volume data. **For developer debugging only; must be removed in production release.**

### Greenhouse Management
- **Description**: Endpoints for monitoring and managing conditions within the greenhouse.
- **Endpoints**:
  - **GET `/greenhouse/data/<date>`**: Displays all environmental data for a specific date.
    - **Response**:
      ```json
      {
        "id": 404,
        "date": "2024-07-12",
        "temperature": 22.5,
        "humidity": 48.0
      }
      ```
  - **GET `/greenhouse/data/range/<start_date>/<end_date>`**: Displays environmental data for a specified date range.
    - **Response**:
      ```json
      [
        {
          "id": 405,
          "date": "2024-07-10",
          "temperature": 21.0,
          "humidity": 50.0
        },
        {
          "id": 406,
          "date": "2024-07-11",
          "temperature": 23.0,
          "humidity": 46.0
        }
      ]
      ```
  - **POST `/greenhouse/data`**: Creates new environmental data. **For developer debugging only; must be removed in production release.**


## Contributing

Contributions are welcome! Please read our CONTRIBUTING.md for details on the process for submitting pull requests.

## Authors

- **Benjamin Leiding** - Product Owner
- **Johannes Mayer** - Scrum Master
- **Mattes Knigge** - Head Developer
- **Izzeldeen Alzeer** - Developer

## License

This project is licensed under the XYZ License - see the [LICENSE.md](LICENSE) file for details.

## Diagrams

### System Overview Diagram

This diagram provides an overview of the main components and workflow of the SmartGreenhouse.

![System Overview](diagrams/Farmbot%20-%20ComponentDiagram.jpg)

### Deployment Diagram

This diagram details the deployment architecture of the SmartGreenhouse software and hardware components.

![Deployment Diagram](diagrams/Farmbot%20-%20Deployment%20Diagram.jpeg)

### Domain Model

This diagram presents the domain model of the SmartGreenhouse, illustrating the main entities and their relationships.

![Domain Model](diagrams/Farmbot%20-%20Domain%20Model.jpeg)

### Electrical Layout of the Greenhouse

This diagram shows the electrical layout of the SmartGreenhouse, detailing the wiring and connections for automation.

![Electrical Layout](diagrams/Farmbot%20-%20Smart%20GreenHouse%20electrical%20layout.jpg)

### Adding New Tasks to the Scheduler

Developers can add new tasks to the `SchedulerService` to automate additional functionalities as needed. Here’s how to add a new task:

1. **Import the Scheduler Service**:
   ```python
   from Scheduler.SchedulerClass import SchedulerService
   ```

2. **Create a Scheduler Instance** (if not already created):
   ```python
   scheduler_service = SchedulerService()
   ```

3. **Define the Task Function**:
   ```python
   def custom_task():
       print("Performing a custom scheduled task.")
   ```

4. **Schedule the New Task**:
   ```python
   scheduler_service.add_job(custom_task, 'interval', hours=1)  # Runs every hour
   ```

5. **Start the Scheduler** (if not already started):
   ```python
   scheduler_service.start()
   ```

This allows for flexible task scheduling based on the specific needs of the greenhouse, enhancing automation and efficiency.
