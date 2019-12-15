from sqlalchemy import create_engine, Column, String, Integer, Date, ForeignKey, ARRAY, TIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

db_url = 'postgres://wgkzeing:gLLwOkOuTVZz3YDPmdzPgW4qA0Ug2cg_@manny.db.elephantsql.com:5432/wgkzeing'
db = create_engine(db_url)

Base = declarative_base()


class Master(Base):
    __tablename__ = 'master'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    start_work_time = Column(TIME, nullable=False)
    days = Column(ARRAY(String), nullable=False)
    appointment_duration_minutes = Column(Integer, nullable=False)
    email = Column(String)

    tasks = relationship('Appointment')

    def __init__(self, id, name, phone_number, start_work_time, days, appointment_duration_minutes, email=None):
        self.id = id
        self.name = name
        self.phone_number = phone_number
        self.start_work_time = start_work_time
        self.days = days
        self.appointment_duration_minutes = appointment_duration_minutes
        self.email = email


class Client(Base):
    __tablename__ = 'client'

    chat_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String)

    tasks = relationship('Appointment')

    def __init__(self, chat_id, name, phone_number, email=None):
        self.chat_id = chat_id
        self.name = name
        self.phone_number = phone_number
        self.email = email


class Appointment(Base):
    __tablename__ = 'appointment'

    id = Column(Integer, primary_key=True)
    start_time = Column(TIME, nullable=False)
    date = Column(Date, nullable=False)
    description = Column(String)
    client_id = Column(Integer, ForeignKey('client.chat_id'), nullable=False)
    master_id = Column(Integer, ForeignKey('master.id'), nullable=False)

    def __init__(self, id, start_time, date, client_id, master_id, description=None):
        self.id = id
        self.start_time = start_time
        self.date = date
        self.client_id = client_id
        self.master_id = master_id
        self.description = description


Session = sessionmaker(db)
session = Session()

Base.metadata.create_all(db)
