from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
 
 Base = declarative_base()
class Symptom(Base):
    __tablename__ = 'symptoms'
    id = Column(Integer, primary_key= True)
    name_symptom = Column(String(20))
    desc_symptom = Column(String(100))
    val_symptom = Column(String(10))
    type_symptom = Column(String(10))

class Action (Base):
    __tablename__ = 'actions'
    id = Column(Integer, primary_key = True)
    order = Column(Integer)
    action_type = Column(String(20))
    name_action = Column(String(20))
    true_false_action = Column(Boolean)
    precondition = Column(String(20))

class Protocol(Base):
    __tablename__ = 'protocols'
    id =  Column(Integer, primary_key=True)
    name_protocol =Column(String(20))
    desc_protocol = Column(String(100))
    type_protocol = Column(String(10))   
    actors = relationship("Actor", secondary='uplet')


class Actor(Base):
    __tablename__ = 'actors'
    id = Column(Integer, primary_key = True)
    role_actor = Column(String(20))
    desc_actor = Column(String(20))
    protocols = relationship(Protocol, secondary='uplet')

class Hypothesis(Base):
    __tablename__='hypothesis'
    id = Column(Integer, primary_key = True)
    name_hypothesis =  Column(String(20))
    desc_hypothesis =  Column(String(100))
    true_false_hypothesis = Column(Boolean)
    protocol_id = Column(Integer, ForeignKey('protocols.id'))
    protocols = relationship('Protocol',back_populates='protocols')


class Case(Base):
    __tablename__ = 'cases'
    id = Column(Integer, primary_key =True)
    name_patient = Column(String(20))
    age_patient = Column(Integer)
    gender_patient = Column(String(10))
    desc_case = Column(String(100))
    symptom_id =  Column(Integer, ForeignKey('symptoms.id'))
    hypothesis_id = Column(Integer, ForeignKey("hypothesis.id"))
    symptoms = relationship('Symptom',back_populates='symptoms')
    hypothesis = relationship('Hypothesis', back_populates='hypothesis')


engine = create_engine('sqlite:///hippocrate.db', echo=True)