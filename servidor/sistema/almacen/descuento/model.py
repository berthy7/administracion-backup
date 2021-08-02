from servidor.database.models import Base
from servidor.database.serializable import Serializable
from sqlalchemy import Column, String, Boolean,DateTime, BigInteger,Float
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

class Descuento(Serializable, Base):
    way = {'personal': {},'responsable': {},'motivo': {}}

    __tablename__ = 'almacen_descuento'

    id = Column(BigInteger, primary_key=True)
    fecha = Column(DateTime, nullable=True)
    tipo = Column(String(20), nullable=False) #Descuento,Sancion
    nroboleta = Column(String(100), nullable=True)
    fkpersonal = Column(BigInteger, ForeignKey("rrhh_personal.id"), nullable=True)
    fkresponsable = Column(BigInteger, ForeignKey("rrhh_personal.id"), nullable=True)

    fkmotivo = Column(BigInteger, ForeignKey("rrhh_motivo.id"), nullable=True)
    material = Column(String(100), nullable=True)
    observacion = Column(String(255), nullable=False)
    monto = Column(Float, nullable=True)

    personal = relationship('Personal', foreign_keys=[fkpersonal])
    responsable = relationship('Personal', foreign_keys=[fkresponsable])
    motivo = relationship('Motivo')

    estado = Column(Boolean, default=True)
    enabled = Column(Boolean, default=True)
