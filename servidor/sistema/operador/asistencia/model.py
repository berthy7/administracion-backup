from servidor.database.models import Base
from servidor.database.serializable import Serializable
from sqlalchemy import Column, String, Boolean, BigInteger,DateTime
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship


class Asistencia(Serializable, Base):
    way = {'personal': {},'cliente': {},'tipoausencia': {}}

    __tablename__ = 'operador_asistencia'

    id = Column(BigInteger, primary_key=True)
    fechar = Column(DateTime, nullable=True)
    fkpersonal = Column(BigInteger, ForeignKey("rrhh_personal.id"), nullable=True)
    fkcliente = Column(BigInteger, ForeignKey("operador_cliente.id"), nullable=True)
    fktipoausencia = Column(BigInteger, ForeignKey("operador_tipoausencia.id"), nullable=True)
    enabled = Column(Boolean, default=True)
    estado = Column(Boolean, default=True)

    personal = relationship('Personal')
    cliente = relationship('Cliente')
    tipoausencia = relationship('TipoAusencia')


class TipoAusencia(Serializable, Base):
    way = {}

    __tablename__ = 'operador_tipoausencia'

    id = Column(BigInteger, primary_key=True)
    nombre = Column(String(255), nullable=False)
    codigo = Column(String(100), nullable=True)
    enabled = Column(Boolean, default=True)
    estado = Column(Boolean, default=True)
