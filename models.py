# coding: utf-8
from sqlalchemy import Boolean, CHAR, CheckConstraint, Column, Date, DateTime, ForeignKey, ForeignKeyConstraint, Integer, Numeric, String, Time
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()
metadata = Base.metadata


class Clinic(Base):
    __tablename__ = 'clinic'
    __table_args__ = (
        CheckConstraint("queue_type = ANY (ARRAY['S'::bpchar, 'I'::bpchar])"),
    )

    cid = Column(String(10), primary_key=True)
    fee = Column(Integer, nullable=False)
    queue_type = Column(CHAR(1), nullable=False)
    acct_name = Column(String(30), nullable=False, unique=True)
    acct_pw = Column(String(100), nullable=False)
    cname = Column(String(30), nullable=False)
    city = Column(String(50), nullable=False)
    district = Column(String(50), nullable=False)
    address = Column(String(100), nullable=False)
    available = Column(Boolean, nullable=False)


class Division(Base):
    __tablename__ = 'division'
    __table_args__ = (
        CheckConstraint("(divname)::text = ANY (ARRAY[('家庭醫學科'::character varying)::text, ('內科'::character varying)::text, ('外科'::character varying)::text, ('兒科'::character varying)::text, ('婦產科'::character varying)::text, ('骨科'::character varying)::text, ('神經科'::character varying)::text, ('神經外科'::character varying)::text, ('泌尿科'::character varying)::text, ('耳鼻喉科'::character varying)::text, ('眼科'::character varying)::text, ('皮膚科'::character varying)::text, ('精神科'::character varying)::text, ('復健科'::character varying)::text, ('麻醉科'::character varying)::text, ('放射診斷科'::character varying)::text, ('放射腫瘤科'::character varying)::text, ('解剖病理科'::character varying)::text, ('臨床病理科'::character varying)::text, ('核子醫學科'::character varying)::text, ('急診醫學科'::character varying)::text, ('整形外科'::character varying)::text, ('職業醫學科'::character varying)::text, ('西醫一般科'::character varying)::text, ('牙醫一般科'::character varying)::text, ('口腔病理科'::character varying)::text, ('口腔顎面外科'::character varying)::text, ('齒顎矯正科'::character varying)::text, ('牙周病科'::character varying)::text, ('兒童牙科'::character varying)::text, ('牙髓病科'::character varying)::text, ('復補綴牙科'::character varying)::text, ('牙體復形科'::character varying)::text, ('家庭牙醫科'::character varying)::text, ('特殊需求者口腔醫學科'::character varying)::text, ('中醫一般科'::character varying)::text, ('中醫內科'::character varying)::text, ('中醫外科'::character varying)::text, ('中醫眼科'::character varying)::text, ('中醫兒科'::character varying)::text, ('中醫婦科'::character varying)::text, ('中醫傷科'::character varying)::text, ('中醫針灸科'::character varying)::text, ('中醫痔科'::character varying)::text])"),
    )

    divid = Column(String(3), primary_key=True)
    divname = Column(String(20), nullable=False, unique=True)


class Doctor(Base):
    __tablename__ = 'doctor'

    docid = Column(String(10), primary_key=True)
    docname = Column(String(20), nullable=False)


class Patient(Base):
    __tablename__ = 'patient'
    __table_args__ = (
        CheckConstraint("gender = ANY (ARRAY['M'::bpchar, 'F'::bpchar])"),
        CheckConstraint("status = ANY (ARRAY['M::bpchar, 'G'::bpchar])")
    )

    pid = Column(String(10), primary_key=True)
    pname = Column(String(100), nullable=False)
    birthdate = Column(Date, nullable=False)
    gender = Column(CHAR(1), nullable=False)
    status = Column(CHAR(1), nullable=False)


class Membership(Base):
    __tablename__ = 'membership'

    pid = Column(ForeignKey('patient.pid', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    acct_pw = Column(String(100), nullable=False)
    email = Column(String(30), nullable=False, unique=True)

    patient = relationship('Patient')


class Clinicdivision(Base):
    __tablename__ = 'clinicdivision'

    divid = Column(ForeignKey('division.divid', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    cid = Column(ForeignKey('clinic.cid', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    available = Column(Boolean, nullable=False)
    queuenumber = Column(Integer)
    lastupdate = Column(DateTime)

    clinic = relationship('Clinic')
    division = relationship('Division')


class Hire(Base):
    __tablename__ = 'hire'

    docid = Column(ForeignKey('doctor.docid', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    cid = Column(ForeignKey('clinic.cid', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    divid = Column(ForeignKey('division.divid', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    startdate = Column(Date)
    enddate = Column(Date)

    clinic = relationship('Clinic')
    division = relationship('Division')
    doctor = relationship('Doctor')


class Period(Base):
    __tablename__ = 'period'
    __table_args__ = (
        CheckConstraint('(weekday >= 1) AND (weekday <= 7)'),
    )

    perid = Column(String(20), primary_key=True)
    cid = Column(ForeignKey('clinic.cid', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    weekday = Column(Integer, nullable=False)
    starttime = Column(Time, nullable=False)
    endtime = Column(Time, nullable=False)
    available = Column(Boolean, nullable=False)

    clinic = relationship('Clinic')


class Room(Base):
    __tablename__ = 'room'

    rid = Column(String(10), primary_key=True, nullable=False)
    cid = Column(ForeignKey('clinic.cid', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    rname = Column(String(5), nullable=False)
    available = Column(Boolean, nullable=False)
    queuenumber = Column(Integer)
    lastupdate = Column(DateTime)

    clinic = relationship('Clinic')


class Searchingrecord(Base):
    __tablename__ = 'searchingrecord'

    recordid = Column(String(20), primary_key=True)
    pid = Column(ForeignKey('patient.pid', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    keyword = Column(String(30))
    plat = Column(Numeric(8, 6))
    plon = Column(Numeric(9, 6))
    divid = Column(String(3))
    city = Column(String(50))
    district = Column(String(50))

    patient = relationship('Patient')


class Treatment(Base):
    __tablename__ = 'treatment'

    tid = Column(String(20), primary_key=True)
    docid = Column(ForeignKey('doctor.docid', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    divid = Column(ForeignKey('division.divid', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    cid = Column(ForeignKey('clinic.cid', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    tname = Column(String(20), nullable=False)
    available = Column(Boolean, nullable=False)

    clinic = relationship('Clinic')
    division = relationship('Division')
    doctor = relationship('Doctor')


class Schedule(Base):
    __tablename__ = 'schedule'

    sid = Column(String(20), primary_key=True)
    divid = Column(ForeignKey('division.divid', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    perid = Column(ForeignKey('period.perid', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    docid = Column(ForeignKey('doctor.docid', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    available = Column(Boolean, nullable=False)

    division = relationship('Division')
    doctor = relationship('Doctor')
    period = relationship('Period')


class Appointment(Base):
    __tablename__ = 'appointment'

    pid = Column(ForeignKey('patient.pid', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    sid = Column(ForeignKey('schedule.sid', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    date = Column(Date, primary_key=True, nullable=False)
    order = Column(Integer, primary_key=True, nullable=False)
    applytime = Column(DateTime, nullable=False)
    status = Column(String(1), nullable=False)
    attendance = Column(Boolean, nullable=False)

    patient = relationship('Patient')
    schedule = relationship('Schedule')


class Reservation(Base):
    __tablename__ = 'reservation'

    pid = Column(ForeignKey('patient.pid', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    sid = Column(ForeignKey('schedule.sid', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    date = Column(Date, primary_key=True, nullable=False)
    applytime = Column(DateTime, nullable=False)
    tid = Column(ForeignKey('treatment.tid', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    status = Column(String(1), nullable=False)
    attendance = Column(Boolean, nullable=False)

    # patient = relationship('Patient')
    schedule = relationship('Schedule')
    treatment = relationship('Treatment')


class Roomschedule(Base):
    __tablename__ = 'roomschedule'
    __table_args__ = (
        ForeignKeyConstraint(['rid', 'cid'], ['room.rid', 'room.cid'], ondelete='CASCADE', onupdate='CASCADE'),
    )

    sid = Column(ForeignKey('schedule.sid', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    rid = Column(String(10), primary_key=True, nullable=False)
    cid = Column(ForeignKey('clinic.cid', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    available = Column(Boolean, nullable=False)

    clinic = relationship('Clinic')
    room = relationship('Room')
    schedule = relationship('Schedule')


class Appointmentremark(Base):
    __tablename__ = 'appointmentremark'
    __table_args__ = (
        ForeignKeyConstraint(['pid', 'sid', 'date', 'order'], ['appointment.pid', 'appointment.sid', 'appointment.date', 'appointment.order'], ondelete='CASCADE', onupdate='CASCADE'),
    )

    pid = Column(ForeignKey('patient.pid', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    sid = Column(ForeignKey('schedule.sid', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    date = Column(Date, primary_key=True, nullable=False)
    order = Column(Integer, primary_key=True, nullable=False)
    text = Column(String(4000), nullable=False)
    datetime = Column(DateTime, primary_key=True, nullable=False)

    appointment = relationship('Appointment')
    patient = relationship('Patient')
    schedule = relationship('Schedule')


class Reservationremark(Base):
    __tablename__ = 'reservationremark'
    __table_args__ = (
        ForeignKeyConstraint(['pid', 'sid', 'date'], ['reservation.pid', 'reservation.sid', 'reservation.date'], ondelete='CASCADE', onupdate='CASCADE'),
    )

    pid = Column(ForeignKey('patient.pid', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    sid = Column(ForeignKey('schedule.sid', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    date = Column(Date, primary_key=True, nullable=False)
    text = Column(String(4000), nullable=False)
    datetime = Column(DateTime, primary_key=True, nullable=False)

    reservation = relationship('Reservation')
    patient = relationship('Patient')
    schedule = relationship('Schedule')
