# ETCE-Farmbot-Smart-Greenhouse

This project includes the backend server for the SmartGreenhouse.
Within the SmartGreenhouse, there is a FarmBot responsible for managing the plants and vegetables.
The backend server, built using Flask, provides several endpoints that enable the monitoring of weather data and management of resources such as water and power for the FarmBot. 
Additionally, the backend integrates with various weather services to fetch real-time data, ensuring optimal growing conditions.
All gathered data is stored in a database, allowing for comprehensive analysis and efficient resource allocation.
This integration aims to create a fully automated and sustainable greenhouse management system.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Weather Forecast Fetching**: Retrieve and store weather forecast data.
- **Weather Station Data Processing**: Fetch and process data from a weather station.
- **Logging and Error Handling**: Detailed logging and error handling for better debugging and monitoring.
- **Database Integration**: Store and manage data in a database.
- **tba**: tba

## Requirements

- all requirements are listed in the `requirements.txt` file

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ETCE-LAB/ETCE-Farmbot-Smart-Greenhouse.git
   cd ETCE-Farmbot-Smart-Greenhouse
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Create a `config.py` file in the root directory and add the following configurations:

```python
# config.py
weather_forecast_url = "YOUR_WEATHER_FORECAST_API_URL"
weatherstation_device_url = "YOUR_WEATHER_STATION_API_URL"
weatherstation_access_key = "YOUR_WEATHER_STATION_ACCESS_KEY"
farmbot_api_key = "YOUR_FARMBOT_API_KEY"
```

## Usage

1. **Run the Flask Application**:
   ```bash
   flask run
   ```
## API Endpoints

### Fetch Weather Forecast

- **Endpoint**: `/forecast/get/<date>`
- **Method**: `GET`
- **Response**:
  ```json
  {
    "id": integer,
    "date": "string",
    "max_temperature": float,
    "min_temperature": float,
    "sunshine_duration_minutes": integer,
    "precipitation_mm": float
  }
  ```

### Fetch Weather Forecast Range

- **Endpoint**: `/forecast/range/<start_date>/<end_date>`
- **Method**: `GET`
- **Response**:
  ```json
  {
    "id": integer,
    "date": "string",
    "max_temperature": float,
    "min_temperature": float,
    "sunshine_duration_minutes": integer,
    "precipitation_mm": float
  },
  {
    "id": integer,
    "date": "string",
    "max_temperature": float,
    "min_temperature": float,
    "sunshine_duration_minutes": integer,
    "precipitation_mm": float
  },
   ...
  ```

### Fetch and Process Data from Weather Station

- **Endpoint**: `/station/data`
- **Method**: `GET`
- **Response**:
  ```json
  {
    "id": integer,
    "measurement_value": float,
    "measurement_type": string,
    "received_at": string
  }
  ```

## Contributing

Contributions are welcome! Please create a pull request or open an issue to discuss any changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
