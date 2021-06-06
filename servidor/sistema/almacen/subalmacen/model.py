from servidor.database.models import Base
from servidor.database.serializable import Serializable
from sqlalchemy import Column, String, Boolean, BigInteger



class SubAlmacen(Serializable, Base):
    way = {}

    __tablename__ = 'almacen_subalmacen'

    id = Column(BigInteger, primary_key=True)
    nombre = Column(String(100), nullable=False)
    estado = Column(Boolean, default=True)
    enabled = Column(Boolean, default=True)

