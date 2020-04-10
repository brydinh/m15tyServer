from db_init import db

from models.modes import Modes

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
    
