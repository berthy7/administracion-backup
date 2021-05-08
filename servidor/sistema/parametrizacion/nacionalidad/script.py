from servidor.database.connection import transaction
from servidor.sistema.usuarios.usuario.model import Modulo
from servidor.sistema.usuarios.rol.model import Rol
from servidor.sistema.parametrizacion.nacionalidad.model import Nacionalidad


def insertions():
    with transaction() as session:
        parametrizacion_m = session.query(Modulo).filter(Modulo.nombre == 'parametrizacion_mod').first()
        if parametrizacion_m is None:
            parametrizacion_m = Modulo(titulo='Parametrizacion', nombre='parametrizacion_mod', icono='business_center')

        nacionalidad_m = session.query(Modulo).filter(Modulo.nombre == 'nacionalidad').first()
        if nacionalidad_m is None:
            nacionalidad_m = Modulo(titulo='Nacionalidad', ruta='/nacionalidad', nombre='nacionalidad', icono='business')

        parametrizacion_m.children.append(nacionalidad_m)

        query_nacionalidad = session.query(Modulo).filter(Modulo.nombre == 'nacionalidad_query').first()
        if query_nacionalidad is None:
            query_nacionalidad = Modulo(titulo='Consultar', ruta='', nombre='nacionalidad_query', menu=False)
        insert_nacionalidad = session.query(Modulo).filter(Modulo.nombre == 'nacionalidad_insert').first()
        if insert_nacionalidad is None:
            insert_nacionalidad = Modulo(titulo='Adicionar', ruta='/nacionalidad_insert', nombre='nacionalidad_insert', menu=False)
        update_nacionalidad = session.query(Modulo).filter(Modulo.nombre == 'nacionalidad_update').first()
        if update_nacionalidad is None:
            update_nacionalidad = Modulo(titulo='Actualizar', ruta='/nacionalidad_update', nombre='nacionalidad_update', menu=False)
        delete_nacionalidad = session.query(Modulo).filter(Modulo.nombre == 'nacionalidad_delete').first()
        if delete_nacionalidad is None:
            delete_nacionalidad = Modulo(titulo='Dar de Baja', ruta='/nacionalidad_delete', nombre='nacionalidad_delete', menu=False)

        nacionalidad_m.children.append(query_nacionalidad)
        nacionalidad_m.children.append(insert_nacionalidad)
        nacionalidad_m.children.append(update_nacionalidad)
        nacionalidad_m.children.append(delete_nacionalidad)

        roles = session.query(Rol).filter(Rol.nombre.in_(['SUPER ADMINISTRADOR', "ADMINISTRADOR"])).all()

        for rol in roles:
            rol.modulos.append(parametrizacion_m)
            rol.modulos.append(nacionalidad_m)
            rol.modulos.append(query_nacionalidad)
            rol.modulos.append(insert_nacionalidad)
            rol.modulos.append(update_nacionalidad)
            rol.modulos.append(delete_nacionalidad)

        session.add(Nacionalidad(nombre='Bolivia'))

        session.commit()
