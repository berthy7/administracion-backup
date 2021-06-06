from servidor.database.models import Base
from servidor.database.serializable import Serializable
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Boolean, BigInteger,ForeignKey



class Almacen(Serializable, Base):
    way = {'subalmacenes': {}}

    __tablename__ = 'almacen_almacen'

    id = Column(BigInteger, primary_key=True)
    nombre = Column(String(100), nullable=False)
    direccion = Column(String(100), nullable=False)
    estado = Column(Boolean, default=True)
    enabled = Column(Boolean, default=True)

    subalmacenes = relationship("AlmacenSubalmacen", cascade="save-update, merge, delete, delete-orphan")



class AlmacenSubalmacen(Serializable, Base):
    way = {'almacen': {},'subalmacen': {}}

    __tablename__ = 'almacen_almacen_subalmacen'

    id = Column(BigInteger, primary_key=True)

    fkalmacen = Column(BigInteger, ForeignKey("almacen_almacen.id"), nullable=True)
    fksubalmacen = Column(BigInteger, ForeignKey("almacen_subalmacen.id"), nullable=True)

    estado = Column(Boolean, default=True)
    enabled = Column(Boolean, default=True)

    almacen = relationship('Almacen')
    subalmacen = relationship('SubAlmacen')