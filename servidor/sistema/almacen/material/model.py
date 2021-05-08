from servidor.database.models import Base
from servidor.database.serializable import Serializable
from sqlalchemy import Column, String, Boolean, BigInteger
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship


class Material(Serializable, Base):
    way = {'tipo': {},'detalle': {}}

    __tablename__ = 'almacen_material'

    id = Column(BigInteger, primary_key=True)
    fktipo = Column(BigInteger, ForeignKey("almacen_material_tipo.id"), nullable=True)
    nombre = Column(String(100), nullable=False)
    cantidad = Column(BigInteger, nullable=True, default=0)
    estado = Column(Boolean, default=True)
    enabled = Column(Boolean, default=True)

    detalle = relationship('MaterialDetalle', cascade="save-update, merge, delete, delete-orphan")
    tipo = relationship('MaterialTipo')

class MaterialDetalle(Serializable, Base):
    way = {'material': {}, 'talla': {}, 'color': {}}

    __tablename__ = 'almacen_material_Detalle'

    id = Column(BigInteger, primary_key=True)
    fkmaterial = Column(BigInteger, ForeignKey("almacen_material.id"), nullable=True)

    fktalla = Column(BigInteger, ForeignKey("almacen_material_talla.id"), nullable=True)
    fkcolor = Column(BigInteger, ForeignKey("almacen_material_color.id"), nullable=True)
    cantidad = Column(BigInteger, nullable=True, default=0)

    estado = Column(Boolean, default=True)
    enabled = Column(Boolean, default=True)

    material = relationship('Material')
    talla = relationship('MaterialTalla')
    color = relationship('MaterialColor')

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