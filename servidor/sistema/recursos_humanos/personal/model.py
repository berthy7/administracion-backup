from servidor.database.models import Base
from servidor.database.serializable import Serializable
from sqlalchemy import Column, String, Boolean, BigInteger,Date,Text
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship


class Personal(Serializable, Base):
    way = {'cargo': {},'expedido': {},'nacionalidad': {},'civil': {},'administrativos': {},'familiares': {},'experiencias': {},'estudios': {},'complementos': {},'documentos': {}}

    __tablename__ = 'rrhh_personal'

    id = Column(BigInteger, primary_key=True)
    nombre = Column(String(100), nullable=False)
    apellidop = Column(String(100), nullable=False)
    apellidom = Column(String(100), nullable=True)
    ci = Column(String(50), nullable=False)
    fechanacimiento = Column(Date, nullable=True)
    fechar = Column(Date, nullable=True)
    telefono = Column(String(100), nullable=True)
    domicilio = Column(String(255), nullable=True)
    foto = Column(Text,nullable=True)
    fkcargo = Column(BigInteger, ForeignKey("rrhh_cargo.id"), nullable=True)

    licenciavehiculo = Column(String(100), nullable=True)
    fkcategoriavehiculo = Column(BigInteger, ForeignKey("parametrizacion_categoria.id"), nullable=True)

    licenciamotocicleta = Column(String(100), nullable=True)
    fkcategoriamotocicleta = Column(BigInteger, ForeignKey("parametrizacion_categoria.id"), nullable=True)

    fkexpedido = Column(BigInteger, ForeignKey('parametrizacion_expedido.id'), nullable=True)
    fknacionalidad = Column(BigInteger, ForeignKey('parametrizacion_nacionalidad.id'), nullable=True)
    fkcivil = Column(BigInteger, ForeignKey('parametrizacion_civil.id'), nullable=True)

    estado = Column(Boolean, default=True)
    enabled = Column(Boolean, default=True)

    categoriavehiculo = relationship("Categoria", foreign_keys=[fkcategoriavehiculo])
    categoriamotocicleta = relationship("Categoria", foreign_keys=[fkcategoriamotocicleta])

    expedido = relationship('Expedido')
    nacionalidad = relationship('Nacionalidad')
    civil = relationship('Civil')
    cargo = relationship('Cargo')

    administrativos = relationship("Administrativo", cascade="save-update, merge, delete, delete-orphan")
    familiares = relationship("Familiar", cascade="save-update, merge, delete, delete-orphan")
    experiencias = relationship("Experiencia", cascade="save-update, merge, delete, delete-orphan")
    estudios = relationship("Estudios", cascade="save-update, merge, delete, delete-orphan")
    complementos = relationship("Complementos", cascade="save-update, merge, delete, delete-orphan")
    documentos = relationship("Documentos", cascade="save-update, merge, delete, delete-orphan")

    @hybrid_property
    def fullname(self):
        aux = ""
        if self.apellidop is not None:
            aux = self.apellidop + " "
        else:
            aux = " "

        if self.apellidom is not None:
            aux = aux + self.apellidom + " "
        else:
            aux = " "

        if self.nombre is not None:
            aux += self.nombre


        if self.fechanacimiento == 'None':
            aux['fechanacimiento'] = None
        else:
            aux['fechanacimiento'] = self.fechanacimiento.strftime('%d/%m/%Y')


        return aux


class Administrativo(Serializable, Base):
    way = {'personal': {},'regimiento': {}}

    __tablename__ = 'rrhh_personal_administrativo'

    id = Column(BigInteger,  primary_key=True)
    fkpersonal = Column(BigInteger, ForeignKey("rrhh_personal.id"))

    serviciomilitar = Column(String(50), nullable=True)
    nrolibreta = Column(String(50), nullable=True)
    fkregimiento = Column(BigInteger, ForeignKey('parametrizacion_regimiento.id'), nullable=True)

    personal = relationship("Personal")
    regimiento = relationship("Regimiento")


class Familiar(Serializable, Base):
    way = {'personal': {},'parentesco': {}}

    __tablename__ = 'rrhh_personal_familiar'

    id = Column(BigInteger, primary_key=True)
    fkpersonal = Column(BigInteger, ForeignKey("rrhh_personal.id"))

    nombre = Column(String(50), nullable=True)
    celular= Column(String(50), nullable=True)
    fkparentesco = Column(BigInteger, ForeignKey('parametrizacion_parentesco.id'), nullable=True)

    personal = relationship("Personal")
    parentesco = relationship('Parentesco')

class Experiencia(Serializable, Base):
    way = {'personal': {},'retiro': {}}

    __tablename__ = 'rrhh_personal_experiencia'

    id = Column(BigInteger, primary_key=True)
    fkpersonal = Column(BigInteger, ForeignKey("rrhh_personal.id"))

    institucion = Column(String(100), nullable=True)
    duracion= Column(String(50), nullable=True)
    fkretiro = Column(BigInteger, ForeignKey('parametrizacion_retiro.id'), nullable=True)
    cargo = Column(String(100), nullable=True)
    telefono = Column(String(100), nullable=True)
    referencia = Column(String(100), nullable=True)

    personal = relationship("Personal")
    retiro = relationship('Retiro')

class Estudios(Serializable, Base):
    way = {'personal': {},'grado': {}}

    __tablename__ = 'rrhh_personal_estudios'

    id = Column(BigInteger, primary_key=True)
    fkpersonal = Column(BigInteger, ForeignKey("rrhh_personal.id"))

    institucion = Column(String(100), nullable=True)
    fkgrado = Column(BigInteger, ForeignKey('parametrizacion_grado.id'), nullable=True)
    egreso = Column(BigInteger, nullable=True)

    personal = relationship("Personal")
    grado = relationship('Grado')

class Complementos(Serializable, Base):
    way = {'personal': {},'grado': {}}

    __tablename__ = 'rrhh_personal_complementos'

    id = Column(BigInteger, primary_key=True)
    fkpersonal = Column(BigInteger, ForeignKey("rrhh_personal.id"))

    estudio = Column(String(255), nullable=True)
    fkgrado = Column(BigInteger, ForeignKey('parametrizacion_grado.id'), nullable=True)

    personal = relationship("Personal")
    grado = relationship('Grado')

class Documentos(Serializable, Base):
    way = {'personal': {}}

    __tablename__ = 'rrhh_personal_documentos'

    id = Column(BigInteger,  primary_key=True)
    fkpersonal = Column(BigInteger, ForeignKey("rrhh_personal.id"))

    ci = Column(Text, nullable=True)
    libretamilitar = Column(Text, nullable=True)
    titulobachiller = Column(Text, nullable=True)
    titulotecnico = Column(Text, nullable=True)
    titulolicenciatura = Column(Text, nullable=True)
    flcn = Column(Text, nullable=True)
    flcc = Column(Text, nullable=True)
    flcv = Column(Text, nullable=True)
    luzagua = Column(Text, nullable=True)
    certificadonacimiento = Column(Text, nullable=True)
    otros = Column(Text, nullable=True)

    personal = relationship("Personal")