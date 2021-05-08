from servidor.database.models import Base
from servidor.database.serializable import Serializable
from sqlalchemy import Column, String, Boolean, BigInteger


class Retiro(Serializable, Base):
    way = {}

    __tablename__ = 'parametrizacion_retiro'

    id = Column(BigInteger, primary_key=True)
    nombre = Column(String(50), nullable=False)
    
    estado = Column(Boolean, default=True)
    enabled = Column(Boolean, default=True)
