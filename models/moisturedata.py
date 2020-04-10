from db_init import db

from models.configdata import ConfigData

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


