from db_init import db

class Modes(db.Model):
    '''
    db model to store irrigation modes
    '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    config_data = db.relationship('ConfigData', backref='mode', lazy=True)
    
    def __init__(self, name):
    	self.name = name

