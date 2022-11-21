from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from flask_login import UserMixin,LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default='')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    birthday = db.Column(db.String(50), nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True )
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    marvel_character = db.relationship('MarvelCharacter', backref = 'owner', lazy = True)

    def __init__(self,email,first_name = '', last_name = '', birthday = '', id = '', password = '', token = '', g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self,length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been added to the database!'

class MarvelCharacter(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    alias = db.Column(db.String(150), nullable = True) 
    powers = db.Column(db.String(250))
    history = db.Column(db.String(200), nullable = True)
    allegiance = db.Column(db.String(50), nullable = True)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, alias, powers, history, allegiance, user_token, id = ''):
        self.id = self.set_id()
        self.name = name
        self.alias = alias
        self.powers = powers
        self.history = history
        self.allegiance = allegiance
        self.user_token = user_token
        
    def __repr__(self):
        return f'The following character has been added to your team: {self.name}'

    def set_id(self):
        return (secrets.token_urlsafe())

class MarvelCharacterSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name','alias', 'powers', 'history', 'allegiance']
        
marvel_character_schema = MarvelCharacterSchema()
marvel_characters_schema = MarvelCharacterSchema(many = True)
