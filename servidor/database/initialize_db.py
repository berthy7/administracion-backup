from configparser import ConfigParser
from sqlalchemy.engine import create_engine
from servidor.database import connection
from servidor.database.models import Base
from servidor.sistema.usuarios.rol.script import insertions as rol_insertions
from servidor.sistema.usuarios.usuario.script import insertions as user_insertions
from servidor.sistema.usuarios.bitacora.script import insertions as log_insertions

from servidor.sistema.parametrizacion.categoria.script import insertions as categoria_insertions
from servidor.sistema.parametrizacion.civil.script import insertions as civil_insertions
from servidor.sistema.parametrizacion.expedido.script import insertions as expedido_insertions
from servidor.sistema.parametrizacion.grado.script import insertions as grado_insertions
from servidor.sistema.parametrizacion.nacionalidad.script import insertions as nacionalidad_insertions
from servidor.sistema.parametrizacion.parentesco.script import insertions as parentesco_insertions
from servidor.sistema.parametrizacion.retiro.script import insertions as retiro_insertions
from servidor.sistema.parametrizacion.regimiento.script import insertions as regimiento_insertions

from servidor.sistema.recursos_humanos.personal.script import insertions as personal_insertions
from servidor.sistema.recursos_humanos.cargo.script import insertions as cargo_insertions


from servidor.sistema.almacen.asignacion.script import insertions as asignacion_insertions
from servidor.sistema.almacen.material.script import insertions as material_insertions
from servidor.sistema.almacen.stock.script import insertions as stock_insertions
from servidor.sistema.almacen.tipomaterial.script import insertions as tipomaterial_insertions

from servidor.sistema.operador.asistencia.script import insertions as asistencia_insertions
from servidor.sistema.operador.cliente.script import insertions as cliente_insertions




import sys
import sqlite3


def main():
    reload_db()
    rol_insertions()
    user_insertions()
    log_insertions()

    categoria_insertions()
    civil_insertions()
    expedido_insertions()
    grado_insertions()

    nacionalidad_insertions()
    parentesco_insertions()
    retiro_insertions()
    regimiento_insertions()

    personal_insertions()
    cargo_insertions()

    asignacion_insertions()
    stock_insertions()
    material_insertions()
    tipomaterial_insertions()

    asistencia_insertions()
    cliente_insertions()



    # negocio_insertions()

    print('Base de datos creada/actualizada correctamente!')


def reload_db():
    config = ConfigParser()
    config.read('settings.ini')
    db_url = config['Database']['url']
    connection.db_url = config['Database']['url']

    if 'sqlite' in db_url:
        dbname = db_url.split('///')[1]
        sqlite3.connect(dbname)

    engine = create_engine(config['Database']['url'])
    Base.metadata.drop_all(engine, checkfirst=True)
    Base.metadata.create_all(engine, checkfirst=True)


def clean_db():
    config = ConfigParser()
    config.read('settings.ini')
    db_url = config['Database']['url']
    connection.db_url = config['Database']['url']

    if 'sqlite' in db_url:
        dbname = db_url.split('///')[1]
        sqlite3.connect(dbname)

    engine = create_engine(config['Database']['url'])
    Base.metadata.drop_all(engine, checkfirst=True)
    print("Las tablas de la base de datos se eliminaron correctamente!")


if __name__ == '__main__':
    sys.exit(int(main() or 0))
