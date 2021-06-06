from servidor.database.connection import transaction
from servidor.sistema.usuarios.usuario.model import Modulo
from servidor.sistema.usuarios.rol.model import Rol
from servidor.sistema.almacen.subalmacen.model import SubAlmacen



def insertions():
    with transaction() as session:
        almacenes_m = session.query(Modulo).filter(Modulo.nombre == 'almacen_mod').first()
        if almacenes_m is None:
            almacenes_m = Modulo(titulo='Almacenes', nombre='almacen_mod', icono='business_center')

        subalmacen_m = session.query(Modulo).filter(Modulo.nombre == 'subalmacen').first()
        if subalmacen_m is None:
            subalmacen_m = Modulo(titulo='Sub Almacen', ruta='/subalmacen', nombre='subalmacen', icono='business')

        almacenes_m.children.append(subalmacen_m)

        query_subalmacen = session.query(Modulo).filter(Modulo.nombre == 'subalmacen_query').first()
        if query_subalmacen is None:
            query_subalmacen = Modulo(titulo='Consultar', ruta='', nombre='subalmacen_query', menu=False)
        insert_subalmacen = session.query(Modulo).filter(Modulo.nombre == 'subalmacen_insert').first()
        if insert_subalmacen is None:
            insert_subalmacen = Modulo(titulo='Adicionar', ruta='/subalmacen_insert', nombre='subalmacen_insert', menu=False)
        update_subalmacen = session.query(Modulo).filter(Modulo.nombre == 'subalmacen_update').first()
        if update_subalmacen is None:
            update_subalmacen = Modulo(titulo='Actualizar', ruta='/subalmacen_update', nombre='subalmacen_update', menu=False)
        delete_subalmacen = session.query(Modulo).filter(Modulo.nombre == 'subalmacen_delete').first()
        if delete_subalmacen is None:
            delete_subalmacen = Modulo(titulo='Dar de Baja', ruta='/subalmacen_delete', nombre='subalmacen_delete', menu=False)

        subalmacen_m.children.append(query_subalmacen)
        subalmacen_m.children.append(insert_subalmacen)
        subalmacen_m.children.append(update_subalmacen)
        subalmacen_m.children.append(delete_subalmacen)

        roles = session.query(Rol).filter(Rol.nombre.in_(['SUPER ADMINISTRADOR', "ADMINISTRADOR", "ALMACEN"])).all()

        for rol in roles:
            rol.modulos.append(almacenes_m)
            rol.modulos.append(subalmacen_m)
            rol.modulos.append(query_subalmacen)
            rol.modulos.append(insert_subalmacen)
            rol.modulos.append(update_subalmacen)
            rol.modulos.append(delete_subalmacen)


        session.add(SubAlmacen(id = 1,nombre='Nuevo'))
        session.add(SubAlmacen(id = 2,nombre='Usado'))
        session.add(SubAlmacen(id = 3,nombre='Descarte'))

        session.commit()
