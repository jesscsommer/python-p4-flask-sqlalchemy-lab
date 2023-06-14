from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from datetime import datetime

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Zookeeper(db.Model):
    __tablename__ = 'zookeepers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    birthday = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    animals = db.relationship("Animal", back_populates="zookeeper")

    def __repr__(self):
        return f"""
            Zookeeper #{self.id}:
            Name: {self.name}
            Birthday: {self.birthday}
            Animals: {self.animals}
        """

class Enclosure(db.Model):
    __tablename__ = 'enclosures'
    __table_args__ = (
        db.CheckConstraint("environment IN (\'Pond\', \'Ocean\', \'Field\', \'Trees\', \'Cave\', \'Cage\', \'Desert\')", 
                            name="env_check"),

    )
    id = db.Column(db.Integer, primary_key=True)
    environment = db.Column(db.String, nullable=False)
    open_to_visitors = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    animals = db.relationship("Animal", back_populates="enclosure")

    def __repr__(self):
        return f"""
            Enclosure #{self.id}:
            Environment: {self.environment}
            Open to visitors: {self.open_to_visitors}
            Animals: {self.animals}
        """

class Animal(db.Model):
    __tablename__ = 'animals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    species = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    zookeeper_id = db.Column(db.Integer, db.ForeignKey('zookeepers.id'))
    enclosure_id = db.Column(db.Integer, db.ForeignKey('enclosures.id'))

    zookeeper = db.relationship("Zookeeper", back_populates="animals")
    enclosure = db.relationship("Enclosure", back_populates="animals")

    def __repr__(self):
        return f"""
            Animal #{self.id}:
            Name: {self.name}
            Species: {self.species} 
            Zookeeper: {self.zookeeper_id} 
            Enclosure: {self.enclosure_id} 
        """