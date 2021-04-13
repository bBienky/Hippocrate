
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///hippocrate.db', echo=True)
Base = declarative_base()

class Symptom(Base):
    __tablename__ = 'symptoms'
    id = Column(Integer, primary_key= True)
    name_symptom = Column(String(20))
    desc_symptom = Column(String(100))
    val_symptom = Column(String(10))
    type_symptom = Column(String(10))
    case_id = Column(Integer, ForeignKey("cases.id"))

class Action (Base):
    __tablename__ = 'actions'
    id = Column(Integer, primary_key = True)
    order = Column(Integer)
    desc_action = Column(String(30), default = "N/A")
    name_action = Column(String(20))
    true_false_action = Column(Boolean)
    precondition = Column(String(20), default = "N/A")
    uplet_id = Column(Integer, ForeignKey("uplet.id"))

class Protocol(Base):
    __tablename__ = 'protocols'
    id =  Column(Integer, primary_key=True)
    name_protocol =Column(String(20))
    desc_protocol = Column(String(100))
    type_protocol = Column(String(10))   
    actor_list = relationship("Uplet")
    hpothes_id = Column(Integer, ForeignKey("hypothesis.id"))


class Actor(Base):
    __tablename__ = 'actors'
    id = Column(Integer, primary_key = True)
    role_actor = Column(String(20))
    name = Column(String(20))

class Hypothesis(Base):
    __tablename__='hypothesis'
    id = Column(Integer, primary_key = True)
    name_hypothesis =  Column(String(20))
    desc_hypothesis =  Column(String(100))
    true_false_hypothesis = Column(Boolean)
    protocol_list = relationship('Protocol')
    case_id = Column(Integer, ForeignKey("cases.id"))


class Case(Base):
    __tablename__ = 'cases'
    id = Column(Integer, primary_key =True)
    name_patient = Column(String(20))
    age_patient = Column(Integer)
    gender_patient = Column(String(10))
    desc_case = Column(String(100))
    type_case = Column(String(20))
    symptoms = relationship('Symptom')
    hypothesis_list = relationship('Hypothesis')

class Uplet(Base):
    __tablename__ = 'uplet'
    id =  Column(Integer, primary_key =True)
    protocol_id = Column(Integer, ForeignKey('protocols.id'))
    actor_id = Column(Integer, ForeignKey('actors.id'))
    action_all = relationship('Action')  
    actors_all = relationship("Actor")
Base.metadata.create_all(engine)