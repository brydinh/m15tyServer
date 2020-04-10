from db_init import db

from models.configdata import ConfigData

class WeatherData(db.Model):
    '''
    db model to store weather info.
    '''
    id = db.Column(db.Integer, primary_key=True)
    posted_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    chance_rain = db.Column(db.Float, nullable=False)
    cloud_conditions = db.Column(db.String(100), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    config_id = db.Column(db.Integer, db.ForeignKey('config_data.id'), nullable=False)

    def __init__(self, chance_rain, cloud_conditions, temperature, humidity):
        self.chance_rain = chane_rain
        self.cloud_conditions = chance_conditions
        self.temperature = temperature
        self.humidity = humidity

