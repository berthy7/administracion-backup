from servidor.database.models import Base
from servidor.database.serializable import Serializable
from sqlalchemy import Column, String, Boolean, BigInteger,DateTime
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship


class Capacitacion(Serializable, Base):
    way = {'integrantes': {'personal': {}}}

    __tablename__ = 'rrhh_capacitacion'

    id = Column(BigInteger, primary_key=True)
    tema = Column(String(255), nullable=False)
    fecha = Column(DateTime, nullable=True)
    relator = Column(String(255), nullable=False)

    estado = Column(Boolean, default=True)
    enabled = Column(Boolean, default=True)

    integrantes = relationship('Integrantes', cascade="save-update, merge, delete, delete-orphan")




class Integrantes(Serializable, Base):
    way = {'personal': {},'capacitacion': {}}

    __tablename__ = 'rrhh_capacitacion_integrantes'

    id = Column(BigInteger,  primary_key=True)
    fkcapacitacion = Column(BigInteger, ForeignKey("rrhh_capacitacion.id"))
    fkpersonal = Column(BigInteger, ForeignKey("rrhh_personal.id"))

    participo = Column(Boolean, nullable=True)
    observacion = Column(String(255), nullable=True,)

    personal = relationship("Personal")
    capacitacion = relationship("Capacitacion")
