from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_marshmallow import Marshmallow
import os
from datetime import datetime

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Modes(db.Model):
    '''
    db model to store irrigation modes
    '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    config_data = db.relationship('ConfigData', backref='configs', lazy=True)
    #config_data = db.relationship('ConfigData', back_populates="mode")
    
    def __init__(self, name):
    	self.name = name

class ConfigData(db.Model):
    '''
    db model to store user configs.
    '''
    id = db.Column(db.Integer, primary_key=True)
    posted_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    timer_length = db.Column(db.Integer)
    # formatted MTWRFSU, MWF, etc.
    scheduled_days = db.Column(db.String(100))
    # formatted as military time (14:20)
    start_time = db.Column(db.String(100))
    is_weather = db.Column(db.Boolean)
    is_moist = db.Column(db.Boolean)
    is_memeified = db.Column(db.Boolean)
    moisture_threshold = db.Column(db.Float)
    rain_threshold = db.Column(db.Float)
    weather_data = db.relationship('WeatherData', backref='postedAt', lazy=True)
    moisture_data = db.relationship('MoistureData', backref='postedAt', lazy=True)
    mode_id = db.Column(db.Integer, db.ForeignKey('modes.id'), nullable=False)
        
    def __init__(self, timer_length, scheduled_days, start_time, is_weather, is_moist, is_memeified, moisture_threshold, rain_threshold, mode_id):
        self.timer_length = timer_length
        self.scheduled_days = scheduled_days
        self.start_time = start_time
        self.is_weather = is_weather
        self.is_moist = is_moist
        self.is_memeified = is_memeified
        self.moisture_threhold = moisture_threshold
        self.rain_threshold = rain_threshold
        self.mode_id = mode_id
            
class MoistureData(db.Model):
    '''
    db model to store sensor moisture info.
    '''
    id = db.Column(db.Integer, primary_key=True)
    posted_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    moisture_level = db.Column(db.Float, nullable=False)
    config_id = db.Column(db.Integer, db.ForeignKey('config_data.id'), nullable=False)

    def __init__(self, moisture_level):
        self.moisture_level = moisture_level


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

class ModeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')

class ConfigSchema(ma.Schema):
    class Meta:
        fields = ('id', 'posted_at', 'timer_length', 
                  'scheduled_days', 'start_time', 'is_weather', 
                  'is_moist', 'is_memeified', 'moisture_threshold',
                  'rain_threshold', "mode_id")

class MoistureSchema(ma.Schema):
    class Meta:
        fields = ('id', 'posted_at', 'moisture_level')

class WeatherSchema(ma.Schema):
    class Meta:
        fields = ('id,' 'posted_at', 'chance_rain', 'cloud_conditions',
                  'temperature', 'humidity')


config_schema = ConfigSchema()
configs_schema = ConfigSchema(many=True)
modes_schema = ModeSchema(many=True)

# add new configuration entry
@app.route('/add_config', methods=['POST'])
def add_config_data():
    timer_length = request.json['timer_length']
    scheduled_days = request.json['scheduled_days']
    start_time = request.json['start_time']
    is_weather = request.json['is_weather']
    is_moist = request.json['is_moist']
    is_memeified = request.json['is_memeified']
    moisture_threshold = request.json['moisture_threshold']
    rain_threshold = request.json['rain_threshold']
    mode_name = request.json['mode_name']


    new_config_entry = ConfigData(timer_length, scheduled_days, start_time, is_weather, 
                                  is_moist, is_memeified, moisture_threshold,
                                  rain_threshold, mode_name)


    db.session.add(new_config_entry)
    db.session.commit()

    return config_schema.jsonify(new_config_entry)

# get all config data
@app.route('/config', methods=['GET'])
def get_all_config_data():
    all_config = ConfigData.query.all()
    result = configs_schema.dump(all_config)
    return jsonify(result)

# get a single config specified by ID
@app.route('/config/<id>', methods=['GET'])
def get_config_data(id):
    config = ConfigData.query.get(id)
    return config_schema.dump(config)

# get most recent config
@app.route('/config/recent', methods=['GET'])
def get_recent_config():
    config = ConfigData.query.order_by(desc('id')).first()
    return config_schema.dump(config)

# get all modes
@app.route('/modes', methods=['GET'])
def get_all_modes():
   all_modes = Modes.query.all()
   result = modes_schema.dump(all_modes)
   return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
