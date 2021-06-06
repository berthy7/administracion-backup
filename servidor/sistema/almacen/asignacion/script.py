from servidor.database.connection import transaction
from servidor.sistema.usuarios.usuario.model import Modulo
from servidor.sistema.usuarios.rol.model import Rol


def insertions():
    with transaction() as session:
        almacen_m = session.query(Modulo).filter(Modulo.nombre == 'almacen_mod').first()
        if almacen_m is None:
            almacen_m = Modulo(titulo='Almacen', nombre='almacen_mod', icono='business_center')

        asignacion_m = session.query(Modulo).filter(Modulo.nombre == 'asignacion').first()
        if asignacion_m is None:
            asignacion_m = Modulo(titulo='Entrega de material', ruta='/asignacion', nombre='asignacion', icono='business')

        almacen_m.children.append(asignacion_m)

        query_asignacion = session.query(Modulo).filter(Modulo.nombre == 'asignacion_query').first()
        if query_asignacion is None:
            query_asignacion = Modulo(titulo='Consultar', ruta='', nombre='asignacion_query', menu=False)
        insert_asignacion = session.query(Modulo).filter(Modulo.nombre == 'asignacion_insert').first()
        if insert_asignacion is None:
            insert_asignacion = Modulo(titulo='Adicionar', ruta='/asignacion_insert', nombre='asignacion_insert', menu=False)
        update_asignacion = session.query(Modulo).filter(Modulo.nombre == 'asignacion_update').first()
        if update_asignacion is None:
            update_asignacion = Modulo(titulo='Actualizar', ruta='/asignacion_update', nombre='asignacion_update', menu=False)
        delete_asignacion = session.query(Modulo).filter(Modulo.nombre == 'asignacion_delete').first()
        if delete_asignacion is None:
            delete_asignacion = Modulo(titulo='Dar de Baja', ruta='/asignacion_delete', nombre='asignacion_delete', menu=False)

        asignacion_m.children.append(query_asignacion)
        asignacion_m.children.append(insert_asignacion)
        asignacion_m.children.append(update_asignacion)
        asignacion_m.children.append(delete_asignacion)

        roles = session.query(Rol).filter(Rol.nombre.in_(['SUPER ADMINISTRADOR', "ADMINISTRADOR", "ALMACEN"])).all()

        for rol in roles:
            rol.modulos.append(almacen_m)
            rol.modulos.append(asignacion_m)
            rol.modulos.append(query_asignacion)
            rol.modulos.append(insert_asignacion)
            rol.modulos.append(update_asignacion)
            rol.modulos.append(delete_asignacion)



        session.commit()
