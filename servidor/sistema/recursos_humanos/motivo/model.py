from servidor.database.models import Base
from servidor.database.serializable import Serializable
from sqlalchemy import Column, String, Boolean, BigInteger,Float
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship


class Motivo(Serializable, Base):
    way = {}

    __tablename__ = 'rrhh_motivo'

    id = Column(BigInteger, primary_key=True)
    nombre = Column(String(150), nullable=False)
    tipo = Column(String(20), nullable=False)  # Descuento,Sancion
    monto = Column(Float, nullable=True, default = 0)

    estado = Column(Boolean, default=True)
    enabled = Column(Boolean, default=True)


