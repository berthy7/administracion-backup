from servidor.database.models import Base
from servidor.database.serializable import Serializable
from sqlalchemy import Column, String, Boolean, BigInteger
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship


class Cargo(Serializable, Base):
    way = {}

    __tablename__ = 'rrhh_cargo'

    id = Column(BigInteger, primary_key=True)
    nombre = Column(String(255), nullable=False)
    estado = Column(Boolean, default=True)
    enabled = Column(Boolean, default=True)


