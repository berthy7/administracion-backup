from servidor.database.models import Base
from servidor.database.serializable import Serializable
from sqlalchemy import Column, String, Boolean, BigInteger
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship


class Material(Serializable, Base):
    way = {'tipo': {},'detalle': {'materialdetallestock': {}}}

    __tablename__ = 'almacen_material'

    id = Column(BigInteger, primary_key=True)
    fktipo = Column(BigInteger, ForeignKey("almacen_material_tipo.id"), nullable=True)
    nombre = Column(String(100), nullable=False)
    estado = Column(Boolean, default=True)
    enabled = Column(Boolean, default=True)

    detalle = relationship('MaterialDetalle', cascade="save-update, merge, delete, delete-orphan")
    tipo = relationship('MaterialTipo')

class MaterialDetalle(Serializable, Base):
    way = {'material': {},'materialdetallestock': {}, 'talla': {}, 'color': {}}

    __tablename__ = 'almacen_material_Detalle'

    id = Column(BigInteger, primary_key=True)
    fkmaterial = Column(BigInteger, ForeignKey("almacen_material.id"), nullable=True)

    fktalla = Column(BigInteger, ForeignKey("almacen_material_talla.id"), nullable=True, default=1)
    fkcolor = Column(BigInteger, ForeignKey("almacen_material_color.id"), nullable=True, default=1)

    estado = Column(Boolean, default=True)
    enabled = Column(Boolean, default=True)

    material = relationship('Material')
    talla = relationship('MaterialTalla')
    color = relationship('MaterialColor')
    materialdetallestock = relationship('MaterialAlmacenStock')

class MaterialTipo(Serializable, Base):
    way = {}

    __tablename__ = 'almacen_material_tipo'

    id = Column(BigInteger, primary_key=True)
    nombre = Column(String(50), nullable=False)

    estado = Column(Boolean, default=True)
    enabled = Column(Boolean, default=True)

class MaterialTalla(Serializable, Base):
    way = {}

    __tablename__ = 'almacen_material_talla'

    id = Column(BigInteger, primary_key=True)
    nombre = Column(String(50), nullable=False)

    estado = Column(Boolean, default=True)
    enabled = Column(Boolean, default=True)

class MaterialColor(Serializable, Base):
    way = {}

    __tablename__ = 'almacen_material_color'

    id = Column(BigInteger, primary_key=True)
    nombre = Column(String(50), nullable=False)

    estado = Column(Boolean, default=True)
    enabled = Column(Boolean, default=True)


class MaterialAlmacenStock(Serializable, Base):
    way = {'material': {}, 'subalmacen': {}}

    __tablename__ = 'almacen_material_almacenstock'

    id = Column(BigInteger, primary_key=True)
    fkdetallematerial = Column(BigInteger, ForeignKey("almacen_material_Detalle.id"), nullable=True)
    fksubalmacen = Column(BigInteger, ForeignKey("almacen_almacen_subalmacen.id"), nullable=True)
    cantidad = Column(BigInteger, nullable=True, default=0)

    estado = Column(Boolean, default=True)
    enabled = Column(Boolean, default=True)

    material = relationship('MaterialDetalle')
    subalmacen = relationship('AlmacenSubalmacen')

