from sqlalchemy import create_engine, Column, String, Integer, Date, ForeignKey, ARRAY, TIME, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

DB_URL = 'postgres://goroanya:goroanya99@localhost:5432/donbo'
DB = create_engine(DB_URL, echo=True)

Base = declarative_base()


class Master(Base):
    __tablename__ = 'master'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    start_work_time = Column(TIME, nullable=False)
    end_work_time = Column(TIME, nullable=False)
    days = Column(ARRAY(String), nullable=False)
    appointment_duration_minutes = Column(Integer, nullable=False)
    email = Column(String)

    tasks = relationship('Appointment')

    def __init__(self, id, name, phone_number, start_work_time,
                 end_work_time, days, appointment_duration_minutes,
                 email=None):
        self.id = id
        self.name = name
        self.phone_number = phone_number
        self.start_work_time = start_work_time
        self.end_work_time = end_work_time
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
    end_time = Column(TIME, nullable=False)
    date = Column(Date, nullable=False)
    description = Column(String)
    client_id = Column(Integer, ForeignKey('client.chat_id', ondelete="SET NULL"), nullable=False)
    master_id = Column(Integer, ForeignKey('master.id', ondelete="SET NULL"), nullable=False)
    notified = Column(Boolean, default=False)

    def __init__(self, start_time, end_time, date, client_id, master_id, description=None):
        self.start_time = start_time
        self.end_time = end_time
        self.date = date
        self.client_id = client_id
        self.master_id = master_id
        self.description = description


Session = sessionmaker(DB)
session = Session()

Base.metadata.create_all(DB)
