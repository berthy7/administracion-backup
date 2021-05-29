from servidor.database.models import Base
from servidor.database.serializable import Serializable
from sqlalchemy import Column, String, Boolean, BigInteger


class Ajuste(Serializable, Base):
    way = {}

    __tablename__ = 'usuarios_ajuste'

    id = Column(BigInteger, primary_key=True)
    claveSecreta = Column(String(150), nullable=False)

    enabled = Column(Boolean, default=True)
