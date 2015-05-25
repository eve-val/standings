from app import db

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1024), index=True, unique=True)
    corporation_id = db.Column(db.Integer, db.ForeignKey('corporation.id'))
    alliance_id = db.Column(db.Integer, db.ForeignKey('alliance.id'))

class Corporation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1024), index=True, unique=True)
    ticker = db.Column(db.String(1024), index=True, unique=True)
    alliance_id = db.Column(db.Integer, db.ForeignKey('alliance.id'))
    characters = db.relationship('Character', backref='corporation', lazy='dynamic')
    standings = db.relationship('Standing', backref='corporation', lazy='dynamic')

class Alliance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1024), index=True, unique=True)
    ticker = db.Column(db.String(1024), index=True, unique=True)
    characters = db.relationship('Character', backref='alliance', lazy='dynamic')
    corporations = db.relationship('Corporation', backref='alliance', lazy='dynamic')
    standings = db.relationship('Standing', backref='alliance', lazy='dynamic')

class Standing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    standing = db.Column(db.String(16), index=True)
    corporation_id = db.Column(db.Integer, db.ForeignKey('corporation.id'))
    alliance_id = db.Column(db.Integer, db.ForeignKey('alliance.id'))
    creator_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    editor_id = db.Column(db.Integer, db.ForeignKey('character.id'))

class StandingChange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    corporation_id = db.Column(db.Integer, db.ForeignKey('corporation.id'))
    alliance_id = db.Column(db.Integer, db.ForeignKey('alliance.id'))
    date = db.Column(db.DateTime)
    character_name = db.Column(db.String(1024))
    character_corporation_name = db.Column(db.String(1024))
    character_corporation_ticker = db.Column(db.String(1024))
    character_alliance_name = db.Column(db.String(1024))
    character_alliance_ticker = db.Column(db.String(1024))

    def find_or_create_corporation_standing(corporation_eve_id, character_eve_id):
        standing = self.query.filter_by(corporation_id = corpororation_eve_id).first()
        if not standing:
            standing = self.__class__()
            
