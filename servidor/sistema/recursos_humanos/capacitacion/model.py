from servidor.database.models import Base
from servidor.database.serializable import Serializable
from sqlalchemy import Column, String, Boolean, BigInteger,DateTime
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship


class Capacitacion(Serializable, Base):
    way = {'integrantes': {'personal': {}},'temas': {'tema': {}},'titulo': {}}

    __tablename__ = 'rrhh_capacitacion'

    id = Column(BigInteger, primary_key=True)
    fecha = Column(DateTime, nullable=True)
    instructor = Column(String(255), nullable=False)
    ubicacion = Column(String(255), nullable=False)
    fktitulo = Column(BigInteger, ForeignKey("rrhh_capacitacion_titulo.id"))

    estado = Column(Boolean, default=True)
    enabled = Column(Boolean, default=True)

    integrantes = relationship('Integrantes', cascade="save-update, merge, delete, delete-orphan")
    temas = relationship('CapacitacionTema', cascade="save-update, merge, delete, delete-orphan")
    titulo = relationship("Titulo")

    def get_dict(self, way=None):
        aux = super().get_dict(way)

        if aux['fecha'] == 'None':
            aux['fecha'] = None
        else:
            aux['fecha'] = self.fecha.strftime('%d/%m/%Y')


        if aux['fecha'] == 'None':
            aux['hora'] = None
        else:
            aux['hora'] = self.fecha.strftime('%H:%M')

        return aux


class Integrantes(Serializable, Base):
    way = {'personal': {},'capacitacion': {}}

    __tablename__ = 'rrhh_capacitacion_integrantes'

    id = Column(BigInteger,  primary_key=True)
    fkcapacitacion = Column(BigInteger, ForeignKey("rrhh_capacitacion.id"))
    fkpersonal = Column(BigInteger, ForeignKey("rrhh_personal.id"))

    resultado = Column(Boolean, nullable=True)
    observacion = Column(String(255), nullable=True)

    personal = relationship("Personal")
    capacitacion = relationship("Capacitacion")


class Titulo(Serializable, Base):
    way = {}

    __tablename__ = 'rrhh_capacitacion_titulo'

    id = Column(BigInteger,  primary_key=True)
    nombre = Column(String(255), nullable=True)

    estado = Column(Boolean, default=True)
    enabled = Column(Boolean, default=True)



class CapacitacionTema(Serializable, Base):
    way = {'tema': {},'capacitacion': {}}

    __tablename__ = 'rrhh_capacitaciontema'

    id = Column(BigInteger,  primary_key=True)
    fkcapacitacion = Column(BigInteger, ForeignKey("rrhh_capacitacion.id"))
    fktema = Column(BigInteger, ForeignKey("rrhh_capacitacion_tema.id"))

    tema = relationship("Tema")
    capacitacion = relationship("Capacitacion")

class Tema(Serializable, Base):
    way = {}

    __tablename__ = 'rrhh_capacitacion_tema'

    id = Column(BigInteger,  primary_key=True)
    nombre = Column(String(255), nullable=True)

    estado = Column(Boolean, default=True)
    enabled = Column(Boolean, default=True)

