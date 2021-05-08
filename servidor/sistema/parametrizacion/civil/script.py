from servidor.database.connection import transaction
from servidor.sistema.usuarios.usuario.model import Modulo
from servidor.sistema.usuarios.rol.model import Rol
from servidor.sistema.parametrizacion.civil.model import Civil


def insertions():
    with transaction() as session:
        parametrizacion_m = session.query(Modulo).filter(Modulo.nombre == 'parametrizacion_mod').first()
        if parametrizacion_m is None:
            parametrizacion_m = Modulo(titulo='Parametrizacion', nombre='parametrizacion_mod', icono='business_center')

        civil_m = session.query(Modulo).filter(Modulo.nombre == 'civil').first()
        if civil_m is None:
            civil_m = Modulo(titulo='Civil', ruta='/civil', nombre='civil', icono='business')

        parametrizacion_m.children.append(civil_m)

        query_civil = session.query(Modulo).filter(Modulo.nombre == 'civil_query').first()
        if query_civil is None:
            query_civil = Modulo(titulo='Consultar', ruta='', nombre='civil_query', menu=False)
        insert_civil = session.query(Modulo).filter(Modulo.nombre == 'civil_insert').first()
        if insert_civil is None:
            insert_civil = Modulo(titulo='Adicionar', ruta='/civil_insert', nombre='civil_insert', menu=False)
        update_civil = session.query(Modulo).filter(Modulo.nombre == 'civil_update').first()
        if update_civil is None:
            update_civil = Modulo(titulo='Actualizar', ruta='/civil_update', nombre='civil_update', menu=False)
        delete_civil = session.query(Modulo).filter(Modulo.nombre == 'civil_delete').first()
        if delete_civil is None:
            delete_civil = Modulo(titulo='Dar de Baja', ruta='/civil_delete', nombre='civil_delete', menu=False)

        civil_m.children.append(query_civil)
        civil_m.children.append(insert_civil)
        civil_m.children.append(update_civil)
        civil_m.children.append(delete_civil)

        roles = session.query(Rol).filter(Rol.nombre.in_(['SUPER ADMINISTRADOR', "ADMINISTRADOR"])).all()

        for rol in roles:
            rol.modulos.append(parametrizacion_m)
            rol.modulos.append(civil_m)
            rol.modulos.append(query_civil)
            rol.modulos.append(insert_civil)
            rol.modulos.append(update_civil)
            rol.modulos.append(delete_civil)

        session.add(Civil(nombre='Soltero'))
        session.add(Civil(nombre='Casado'))
        session.add(Civil(nombre='Divorciado'))
        session.add(Civil(nombre='Viudo'))


        session.commit()
