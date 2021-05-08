from servidor.database.models import Base
from servidor.database.serializable import Serializable
from sqlalchemy import Column, String, Boolean, BigInteger
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship


class Cliente(Serializable, Base):
    way = {}

    __tablename__ = 'operador_cliente'

    id = Column(BigInteger, primary_key=True)
    nombre = Column(String(255), nullable=False)
    dia = Column(String(100), nullable=True)
    noche = Column(String(100), default=True)
    enabled = Column(Boolean, default=True)
    estado = Column(Boolean, default=True)

