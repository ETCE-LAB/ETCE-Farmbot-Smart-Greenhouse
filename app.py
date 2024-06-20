from flask import Flask, render_template
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from DataLayer.Models import ApiSchemas

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smart_greenhouse.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

api = Api(app, version='3.0', title='API',
          description='Endpoints for the Smart Greenhouse System by ETCE-LAB',
          doc='/swagger',
          license='README.md',
          license_url='https://github.com/ETCE-LAB/ETCE-Farmbot-Smart-Greenhouse/blob/main/README.md'
          )


@api.documentation
def custom_ui():
    return render_template('swagger_ui.html')


weather_station_model, weather_forecast_model, water_management_model, greenhouse_model = ApiSchemas.create_models(api)


def register_namespaces():
    from Controllers.FarmBotController import farmbot_ns
    from Controllers.WaterManagementController import water_ns
    from Controllers.WeatherStationController import station_ns
    from Controllers.WeatherPredictionController import forecast_ns
    from Controllers.GreenHouseController import greenhouse_ns

    api.add_namespace(station_ns)
    api.add_namespace(forecast_ns)
    api.add_namespace(water_ns)
    api.add_namespace(farmbot_ns)
    api.add_namespace(greenhouse_ns)
    print("Namespaces registered.")


register_namespaces()

if __name__ == '__main__':
    app.run(debug=True)
