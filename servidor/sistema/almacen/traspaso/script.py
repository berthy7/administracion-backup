from servidor.database.connection import transaction
from servidor.sistema.usuarios.usuario.model import Modulo
from servidor.sistema.usuarios.rol.model import Rol



def insertions():
    with transaction() as session:
        almacen_m = session.query(Modulo).filter(Modulo.nombre == 'almacen_mod').first()
        if almacen_m is None:
            almacen_m = Modulo(titulo='Almacen', nombre='almacen_mod', icono='business_center')

        traspaso_m = session.query(Modulo).filter(Modulo.nombre == 'traspaso').first()
        if traspaso_m is None:
            traspaso_m = Modulo(titulo='Traspaso de Material', ruta='/traspaso', nombre='traspaso', icono='business')

        almacen_m.children.append(traspaso_m)

        query_traspaso = session.query(Modulo).filter(Modulo.nombre == 'traspaso_query').first()
        if query_traspaso is None:
            query_traspaso = Modulo(titulo='Consultar', ruta='', nombre='traspaso_query', menu=False)
        insert_traspaso = session.query(Modulo).filter(Modulo.nombre == 'traspaso_insert').first()
        if insert_traspaso is None:
            insert_traspaso = Modulo(titulo='Adicionar', ruta='/traspaso_insert', nombre='traspaso_insert', menu=False)
        update_traspaso = session.query(Modulo).filter(Modulo.nombre == 'traspaso_update').first()
        if update_traspaso is None:
            update_traspaso = Modulo(titulo='Actualizar', ruta='/traspaso_update', nombre='traspaso_update', menu=False)
        delete_traspaso = session.query(Modulo).filter(Modulo.nombre == 'traspaso_delete').first()
        if delete_traspaso is None:
            delete_traspaso = Modulo(titulo='Dar de Baja', ruta='/traspaso_delete', nombre='traspaso_delete', menu=False)

        traspaso_m.children.append(query_traspaso)
        traspaso_m.children.append(insert_traspaso)
        traspaso_m.children.append(update_traspaso)
        traspaso_m.children.append(delete_traspaso)

        roles = session.query(Rol).filter(Rol.nombre.in_(['SUPER ADMINISTRADOR', "ADMINISTRADOR", "ALMACEN"])).all()

        for rol in roles:
            rol.modulos.append(almacen_m)
            rol.modulos.append(traspaso_m)
            rol.modulos.append(query_traspaso)
            rol.modulos.append(insert_traspaso)
            rol.modulos.append(update_traspaso)
            rol.modulos.append(delete_traspaso)

        session.commit()
