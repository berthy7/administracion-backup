from servidor.database.models import Base
from servidor.database.serializable import Serializable
from sqlalchemy import Column, String, Boolean,DateTime, BigInteger,Text
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

class Traspaso(Serializable, Base):
    way = {'detalle': {},'subalmacenorigen': {},'subalmacendestino': {}}

    __tablename__ = 'almacen_traspaso'

    id = Column(BigInteger, primary_key=True)
    fksubalmacenorigen = Column(BigInteger, ForeignKey("almacen_almacen_subalmacen.id"), nullable=True)
    fksubalmacendestino = Column(BigInteger, ForeignKey("almacen_almacen_subalmacen.id"), nullable=True)
    descripcion = Column(Text, nullable=True)
    fechar = Column(DateTime, nullable=True)

    estado = Column(Boolean, default=True)
    enabled = Column(Boolean, default=True)

    subalmacenorigen = relationship('AlmacenSubalmacen', foreign_keys=[fksubalmacenorigen])
    subalmacendestino = relationship('AlmacenSubalmacen', foreign_keys=[fksubalmacendestino])

    detalle = relationship("TraspasoDetalle", cascade="save-update, merge, delete, delete-orphan")


class TraspasoDetalle(Serializable, Base):
    way = {'traspaso': {}, 'materialDetalle': {'color': {},'talla': {}}}

    __tablename__ = 'almacen_traspaso_detalle'

    id = Column(BigInteger, primary_key=True)
    fktraspaso = Column(BigInteger, ForeignKey("almacen_traspaso.id"), nullable=True)
    fkmaterialDetalle = Column(BigInteger, ForeignKey("almacen_material_Detalle.id"), nullable=True)
    cantidad = Column(BigInteger, nullable=True, default=0)

    estado = Column(Boolean, default=True)
    enabled = Column(Boolean, default=True)

    traspaso = relationship('Traspaso')
    materialDetalle = relationship('MaterialDetalle')


