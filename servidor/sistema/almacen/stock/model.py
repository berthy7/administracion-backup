from servidor.database.models import Base
from servidor.database.serializable import Serializable
from sqlalchemy import Column, String, Boolean,DateTime, BigInteger,Text
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship


class Stock(Serializable, Base):
    way = {'detalle': {}}

    __tablename__ = 'almacen_stock'

    id = Column(BigInteger, primary_key=True)
    nroboleta = Column(String(50), nullable=False)
    observacion = Column(Text, nullable=True)
    fechar = Column(DateTime, nullable=True)

    estado = Column(Boolean, default=True)
    enabled = Column(Boolean, default=True)

    detalle = relationship("StockDetalle", cascade="save-update, merge, delete, delete-orphan")


class StockDetalle(Serializable, Base):
    way = {'stock': {}, 'materialDetalle': {'color': {},'talla': {}}}

    __tablename__ = 'almacen_stock_detalle'

    id = Column(BigInteger, primary_key=True)
    fkstock = Column(BigInteger, ForeignKey("almacen_stock.id"), nullable=True)
    fkmaterialDetalle = Column(BigInteger, ForeignKey("almacen_material_Detalle.id"), nullable=True)
    cantidad = Column(String(50), nullable=False)

    estado = Column(Boolean, default=True)
    enabled = Column(Boolean, default=True)

    stock = relationship('Stock')
    materialDetalle = relationship('MaterialDetalle')




