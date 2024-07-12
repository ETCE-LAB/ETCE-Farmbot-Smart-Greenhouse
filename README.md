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

### Weather Station
- **Description**: Endpoints for capturing and processing weather station data.
- **Endpoints**:
  - GET `/station/data/<date>`: Displays weather data for a specific date.
    - **Response**:
      ```json
      {
        "id": 101,
        "measurement_value": 22.5,
        "measurement_type": "Temperature",
        "received_at": "2024-07-12T15:30:00Z"
      }
      ```

### Weather Forecast
- **Description**: Endpoints for querying weather forecasts.
- **Endpoints**:
  - GET `/forecast/<date>`: Retrieves weather forecast data for a specific date.
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

### Water Management
- **Description**: Endpoints for managing water consumption and storage.
- **Endpoints**:
  - GET `/water/volume/<date>`: Displays water volume on a specific date.
    - **Response**:
      ```json
      {
        "id": 303,
        "date": "2024-07-12",
        "volume": 1500.0
      }
      ```

### Greenhouse Management
- **Description**: Endpoints for monitoring and managing conditions within the greenhouse.
- **Endpoints**:
  - GET `/greenhouse/data/<date>`: Displays all environmental data for a specific date.
    - **Response**:
      ```json
      {
        "id": 404,
        "date": "2024-07-12",
        "temperature": 22.5,
        "humidity": 48.0
      }
      ```

## Contributing

Contributions are welcome! Please read our CONTRIBUTING.md for details on the process for submitting pull requests.

## Authors

- **Benjamin Leiding** - Product Owner
- **Johannes Meier** - Scrum Master
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
