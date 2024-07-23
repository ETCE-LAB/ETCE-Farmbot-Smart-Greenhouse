# SmartGreenhouse

## About the Project

SmartGreenhouse aims to create an intelligent greenhouse that captures internal and external environmental conditions using a variety of sensors. The collected data is stored in a database for later analysis. Additionally, the project utilizes collected rainwater to ensure an independent water supply. A central component of the greenhouse is the FarmBot, which fully autonomously tends to the plants from sowing to harvest.

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [Hardware Components](#hardware-components)
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

## Hardware Components


![Electrical Layout](diagrams/Farmbot%20-%20Smart%20GreenHouse%20electrical%20layout.jpg)


1. **[Power Source](https://www.conrad.de/de/p/as-schwabe-38605-steckdosenleiste-mit-schalter-5fach-schwarz-blau-schutzkontakt-1-st-554185.html?hk=SEM&WT.mc_id=google_pla&gad_source=1&gclid=CjwKCAjwqf20BhBwEiwAt7dtdX-ABvpET5O90LvCdpdZUiPzcTarY--6IHyBcgyYU0xdxWVMScb40xoCEgIQAvD_BwE)**
   - Provides the primary electricity supply at 230V, converted to necessary operational voltages: 5V for Raspberry Pis and 12V for pumps and lighting systems.

2. **[Workstation](https://www.conrad.de/de/p/speaka-professional-sp-mm-710-1fach-monitor-wandhalterung-33-0-cm-13-68-6-cm-27-schwarz-hoehenverstellbar-drehba-2588303.html)**
   - Features a USB Type-C docking station connected to a monitor, supporting both power charging and data transmission. Required voltage: 5V.
   - Includes a notebook wall mount for an ergonomic and space-efficient setup.

3. **[Raspberry Pi 5](https://www.reichelt.de/raspberry-pi-5-b-4x-2-4-ghz-4-gb-ram-wlan-bt-rasp-pi-5-b-4gb-p359842.html?PROVID=2788&gad_source=1&gclid=CjwKCAjwqf20BhBwEiwAt7dtdSE7gUMOW9vdfBwd9oaYPYIJHRKJHPYXgpAYMLuem95n4GLVpXiythoC27kQAvD_BwE)**
   - Controls various sensors and hosts the backend system. Required voltage: 5V.

4. **[Temperature and Humidity Sensor](https://amzn.eu/d/0fd29NcE)**
   - Monitors and maintains optimal climate conditions within the greenhouse using the **DHT22 AM2302** sensor.

5. **[Greenhouse Surveillance Camera](https://www.reichelt.com/raspberry-pi-kamera-12mp-76-v3-rasp-cam-3-p339256.html?CCOUNTRY=445&LANGUAGE=de&utm_source=display&utm_medium=rsp-foundation&src=raspberrypi&&r=1)**
   - Enhances security and operational oversight through high-resolution visual monitoring with the **RASP CAM 3**.

6. **[Ultrasonic Water Level Sensor](https://amzn.eu/d/0gpDR76l)**
   - Ensures accurate water levels in tanks with the **HC-SR04** sensor, supporting precise irrigation management.

7. **[FarmBot](https://farm.bot/products/farmbot-genesis-v1-7)**
   - Automates garden management from sowing to harvesting. Required voltage: 12V.

8. **[Sockets and Connections](https://www.conrad.de/de/p/brennenstuhl-1161750020-strom-verlaengerungskabel-gelb-blau-5-00-m-at-n05v3v3-f-3g-1-5-mm-2303709.html)**
   - Provides waterproof sockets and cables for reliable connections and power supply to all system components.

9. **[Pump](https://www.conrad.de/de/p/toolcraft-to-7159158-niedervolt-druckwasserpumpe-1020-l-h-12-v-dc-2386386.html)**
   - Delivers pressurized water to the FarmBot, ensuring adequate water flow. Required voltage: 12V.

10. **[Power Converter for the Pump](https://led-profi.de/led-trafo-netzteil/12v-led-trafos-standard/165498859/led-trafo-12v-180w-15a-mm-pfc-dc-schaltnetzteil-slim-line-ftpc200v12-moebel?c=1929341)**
    - Converts 230V to 12V, providing the pump with the necessary amperage.

11. **[TAPO Sockets](https://www.reichelt.de/de/de/schaltbare-wlan-steckdose-tplink-tapo-p100-p270914.html?PROVID=2788&gad_source=1&gclid=CjwKCAjwhvi0BhA4EiwAX25uj2u371wdbBkpY8luAcP6tm1R22U-9cxW5mjwfDROY-HqNlhTUYKzmxoCkgkQAvD_BwE&&r=1)**
    - Enables control over power sockets via Raspberry Pi, facilitating the management of the pump and other accessories.

12. **[Snail Defense System](https://www.onlineshop-reich.de/garten/schaedlingsbekaempfung/snailstop-elektrischer-schneckenzaun-schnecken-stop-zuverlaessig-und-ohne-gift_30100_4145)**
    - Provides a non-lethal barrier against snails, protecting plants from damage.

13. **[Gardena and Hose Connections](https://www.amazon.de/s?k=gardena+connector+3%2F4&crid=2T1J00APX5BKX&sprefix=gardena+conne%2Caps%2C125&ref=nb_sb_ss_pltr-xclick_3_13)**
    - Features quick connectors and a 3/4-inch hose for seamless integration with the rain barrel and FarmBot systems.

14. **[Rain Barrel](https://www.obi.de/p/6739676/garantia-regentonne-rund-210-l-gruen)**
    - Collects and stores rainwater for efficient irrigation use.

15. **[Float Valve](https://www.siepmann.net/SIMA_Ersatzventil.html)**
    - Automatically tracks the water level in the rain barrel, preventing the pump from running dry.


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
