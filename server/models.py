from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Hero(db.Model,SerializerMixin):
    __tablename__ = 'heroes'

    serialize_rules = ('-hero_powers','-created_at','-updated_at','-powers.heroes')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    hero_powers = db.relationship('HeroPower',backref = 'hero')
    powers = association_proxy('hero_powers','power')

class Power(db.Model,SerializerMixin):
    __tablename__ = 'powers'

    serialize_rules = ('-hero_powers','-created_at','-updated_at','-heroes.created_at','-heroes.updated_at','-heroes.powers')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    hero_powers = db.relationship('HeroPower',backref = 'power')
    heroes = association_proxy('hero_powers','hero')

    @validates('description')
    def validate_description(self,key,description):
        if not description or type(description) != str or len(description) < 20:
            raise ValueError('Description not valid.')
        return description

class HeroPower(db.Model,SerializerMixin):
    __tablename__ = 'hero_powers'

    serialize_rules = ('-hero.hero_powers','-power.hero_powers','-created_at','-updated_at','-power.heroes','-hero.powers')

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    hero_id = db.Column(db.Integer,db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer,db.ForeignKey('powers.id'))

    @validates('strength')
    def validate_strength(self,key,strength):
        category = ['Strong', 'Weak', 'Average']
        if strength not in category:
            raise ValueError('Invalid. Strength must be one of: Strong, Weak, Average')
        return strength

