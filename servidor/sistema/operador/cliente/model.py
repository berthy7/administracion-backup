from servidor.database.models import Base
from servidor.database.serializable import Serializable
from sqlalchemy import Column, String, Boolean, BigInteger,Integer
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship


class Cliente(Serializable, Base):
    way = {'personales': {'personal': {}}}

    __tablename__ = 'operador_cliente'

    id = Column(BigInteger, primary_key=True)
    nombre = Column(String(255), nullable=False)
    codigo = Column(String(100), nullable=True)

    enabled = Column(Boolean, default=True)
    estado = Column(Boolean, default=True)

    personales = relationship("ClientePersonal", cascade="save-update, merge, delete, delete-orphan")


class ClientePersonal(Serializable, Base):
    way = {'turno': {},'personal': {},'cliente': {}}

    __tablename__ = 'operador_cliente_personal'

    id = Column(BigInteger,  primary_key=True)
    fkcliente = Column(BigInteger, ForeignKey('operador_cliente.id'), nullable=True)

    fkpersonal = Column(BigInteger, ForeignKey("rrhh_personal.id"))
    fkturno = Column(BigInteger, ForeignKey("operador_asistencia_turno.id"), nullable=True)

    personal = relationship("Personal")
    cliente = relationship("Cliente")
    turno = relationship('Turno')



