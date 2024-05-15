# ETCE-Farmbot-Smart-Greenhouse

# FarmBot Project

This project integrates a FarmBot with a Flask backend to manage and execute sequences, fetch weather data, and process weather station data. The backend provides several endpoints to interact with the FarmBot and weather services.

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

- **Execute FarmBot Sequences**: Trigger FarmBot sequences through a Flask endpoint.
- **Weather Forecast Fetching**: Retrieve and store weather forecast data.
- **Weather Station Data Processing**: Fetch and process data from a weather station.
- **Logging and Error Handling**: Detailed logging and error handling for better debugging and monitoring.

## Requirements

- Python 3.x
- Flask
- Requests
- SQLAlchemy

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/farmbot-project.git
   cd farmbot-project
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

2. **Trigger a FarmBot Sequence**:
   Use an HTTP client like Postman or `curl` to send a POST request to `/execute-sequence` endpoint with a JSON body containing the `sequence_id`.

## API Endpoints

### Execute Sequence

- **Endpoint**: `/execute-sequence`
- **Method**: `POST`
- **Payload**:
  ```json
  {
      "sequence_id": 123
  }
  ```
- **Response**:
  ```json
  {
      "status": "success",
      "message": "Sequence executed successfully",
      "sequence_id": 123
  }
  ```

### Fetch Weather Forecast

- **Endpoint**: `/fetch-weather-forecast/<date>`
- **Method**: `GET`
- **Response**:
  ```json
  {
      "date": "2024-05-15",
      "max_temperature": 25,
      "min_temperature": 15,
      "sunshine_duration_minutes": 720,
      "precipitation_mm": 5
  }
  ```

### Fetch Weather Forecast Range

- **Endpoint**: `/fetch-weather-forecast-range/<start_date>/<end_date>`
- **Method**: `GET`
- **Response**:
  ```json
  [
      {
          "date": "2024-05-15",
          "max_temperature": 25,
          "min_temperature": 15,
          "sunshine_duration_minutes": 720,
          "precipitation_mm": 5
      },
      "..."
  ]
  ```

### Fetch and Process Data from Weather Station

- **Endpoint**: `/fetch-and-process-data`
- **Method**: `GET`
- **Response**:
  ```json
  {
      "message": "Data fetched and saved successfully",
      "code": 200
  }
  ```

## Contributing

Contributions are welcome! Please create a pull request or open an issue to discuss any changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
