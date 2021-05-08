from servidor.database.connection import transaction
from servidor.sistema.usuarios.usuario.model import Modulo
from servidor.sistema.usuarios.rol.model import Rol
from servidor.sistema.parametrizacion.grado.model import Grado


def insertions():
    with transaction() as session:
        parametrizacion_m = session.query(Modulo).filter(Modulo.nombre == 'parametrizacion_mod').first()
        if parametrizacion_m is None:
            parametrizacion_m = Modulo(titulo='Parametrizacion', nombre='parametrizacion_mod', icono='business_center')

        grado_m = session.query(Modulo).filter(Modulo.nombre == 'grado').first()
        if grado_m is None:
            grado_m = Modulo(titulo='Grado', ruta='/grado', nombre='grado', icono='business')

        parametrizacion_m.children.append(grado_m)

        query_grado = session.query(Modulo).filter(Modulo.nombre == 'grado_query').first()
        if query_grado is None:
            query_grado = Modulo(titulo='Consultar', ruta='', nombre='grado_query', menu=False)
        insert_grado = session.query(Modulo).filter(Modulo.nombre == 'grado_insert').first()
        if insert_grado is None:
            insert_grado = Modulo(titulo='Adicionar', ruta='/grado_insert', nombre='grado_insert', menu=False)
        update_grado = session.query(Modulo).filter(Modulo.nombre == 'grado_update').first()
        if update_grado is None:
            update_grado = Modulo(titulo='Actualizar', ruta='/grado_update', nombre='grado_update', menu=False)
        delete_grado = session.query(Modulo).filter(Modulo.nombre == 'grado_delete').first()
        if delete_grado is None:
            delete_grado = Modulo(titulo='Dar de Baja', ruta='/grado_delete', nombre='grado_delete', menu=False)

        grado_m.children.append(query_grado)
        grado_m.children.append(insert_grado)
        grado_m.children.append(update_grado)
        grado_m.children.append(delete_grado)

        roles = session.query(Rol).filter(Rol.nombre.in_(['SUPER ADMINISTRADOR', "ADMINISTRADOR"])).all()

        for rol in roles:
            rol.modulos.append(parametrizacion_m)
            rol.modulos.append(grado_m)
            rol.modulos.append(query_grado)
            rol.modulos.append(insert_grado)
            rol.modulos.append(update_grado)
            rol.modulos.append(delete_grado)

        session.add(Grado(nombre='Bachiller'))
        session.add(Grado(nombre='Medio'))
        session.add(Grado(nombre='Tecnico'))
        session.add(Grado(nombre='Licenciatura'))

        session.commit()
