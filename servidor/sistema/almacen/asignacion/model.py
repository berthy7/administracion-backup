from servidor.database.models import Base
from servidor.database.serializable import Serializable
from sqlalchemy import Column, String, Boolean,DateTime, BigInteger
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship


class Asignacion(Serializable, Base):
    way = {'personal': {},'detalle': {}}

    __tablename__ = 'almacen_asignacion'

    id = Column(BigInteger, primary_key=True)
    descripcion = Column(String(50), nullable=False)
    fechar = Column(DateTime, nullable=True)
    fkpersonal = Column(BigInteger, ForeignKey("rrhh_personal.id"), nullable=True)

    estado = Column(Boolean, default=True)
    enabled = Column(Boolean, default=True)

    personal = relationship('Personal')
    detalle = relationship("AsignacionDetalle", cascade="save-update, merge, delete, delete-orphan")


class AsignacionDetalle(Serializable, Base):
    way = {'asignacion': {},'materialDetalle': {'color': {},'talla': {}}}

    __tablename__ = 'almacen_asignacion_detalle'

    id = Column(BigInteger, primary_key=True)
    fkasignacion = Column(BigInteger, ForeignKey("almacen_asignacion.id"), nullable=True)
    fkmaterialDetalle = Column(BigInteger, ForeignKey("almacen_material_Detalle.id"), nullable=True)
    cantidad = Column(String(50), nullable=False)

    estado = Column(Boolean, default=True)
    enabled = Column(Boolean, default=True)

    asignacion = relationship('Asignacion')
    materialDetalle = relationship('MaterialDetalle')

