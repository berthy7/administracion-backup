from servidor.database.connection import transaction
from servidor.sistema.usuarios.usuario.model import Modulo
from servidor.sistema.usuarios.rol.model import Rol



def insertions():
    with transaction() as session:
        almacenes_m = session.query(Modulo).filter(Modulo.nombre == 'almacen_mod').first()
        if almacenes_m is None:
            almacenes_m = Modulo(titulo='Almacenes', nombre='almacen_mod', icono='business_center')

        almacen_m = session.query(Modulo).filter(Modulo.nombre == 'almacen').first()
        if almacen_m is None:
            almacen_m = Modulo(titulo='Almacen', ruta='/almacen', nombre='almacen', icono='business')

        almacenes_m.children.append(almacen_m)

        query_almacen = session.query(Modulo).filter(Modulo.nombre == 'almacen_query').first()
        if query_almacen is None:
            query_almacen = Modulo(titulo='Consultar', ruta='', nombre='almacen_query', menu=False)
        insert_almacen = session.query(Modulo).filter(Modulo.nombre == 'almacen_insert').first()
        if insert_almacen is None:
            insert_almacen = Modulo(titulo='Adicionar', ruta='/almacen_insert', nombre='almacen_insert', menu=False)
        update_almacen = session.query(Modulo).filter(Modulo.nombre == 'almacen_update').first()
        if update_almacen is None:
            update_almacen = Modulo(titulo='Actualizar', ruta='/almacen_update', nombre='almacen_update', menu=False)
        delete_almacen = session.query(Modulo).filter(Modulo.nombre == 'almacen_delete').first()
        if delete_almacen is None:
            delete_almacen = Modulo(titulo='Dar de Baja', ruta='/almacen_delete', nombre='almacen_delete', menu=False)

        almacen_m.children.append(query_almacen)
        almacen_m.children.append(insert_almacen)
        almacen_m.children.append(update_almacen)
        almacen_m.children.append(delete_almacen)

        roles = session.query(Rol).filter(Rol.nombre.in_(['SUPER ADMINISTRADOR', "ADMINISTRADOR", "ALMACEN"])).all()

        for rol in roles:
            rol.modulos.append(almacenes_m)
            rol.modulos.append(almacen_m)
            rol.modulos.append(query_almacen)
            rol.modulos.append(insert_almacen)
            rol.modulos.append(update_almacen)
            rol.modulos.append(delete_almacen)

        session.commit()
