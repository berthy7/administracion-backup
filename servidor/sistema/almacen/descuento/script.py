from servidor.database.connection import transaction
from servidor.sistema.usuarios.usuario.model import Modulo
from servidor.sistema.usuarios.rol.model import Rol



def insertions():
    with transaction() as session:
        almacen_m = session.query(Modulo).filter(Modulo.nombre == 'almacen_mod').first()
        if almacen_m is None:
            almacen_m = Modulo(titulo='Almacen', nombre='almacen_mod', icono='business_center')

        descuento_m = session.query(Modulo).filter(Modulo.nombre == 'descuento').first()
        if descuento_m is None:
            descuento_m = Modulo(titulo='Descuentos', ruta='/descuento', nombre='descuento', icono='business')

        almacen_m.children.append(descuento_m)

        query_descuento = session.query(Modulo).filter(Modulo.nombre == 'descuento_query').first()
        if query_descuento is None:
            query_descuento = Modulo(titulo='Consultar', ruta='', nombre='descuento_query', menu=False)
        insert_descuento = session.query(Modulo).filter(Modulo.nombre == 'descuento_insert').first()
        if insert_descuento is None:
            insert_descuento = Modulo(titulo='Adicionar', ruta='/descuento_insert', nombre='descuento_insert', menu=False)
        update_descuento = session.query(Modulo).filter(Modulo.nombre == 'descuento_update').first()
        if update_descuento is None:
            update_descuento = Modulo(titulo='Actualizar', ruta='/descuento_update', nombre='descuento_update', menu=False)
        delete_descuento = session.query(Modulo).filter(Modulo.nombre == 'descuento_delete').first()
        if delete_descuento is None:
            delete_descuento = Modulo(titulo='Dar de Baja', ruta='/descuento_delete', nombre='descuento_delete', menu=False)

        descuento_m.children.append(query_descuento)
        descuento_m.children.append(insert_descuento)
        descuento_m.children.append(update_descuento)
        descuento_m.children.append(delete_descuento)

        roles = session.query(Rol).filter(Rol.nombre.in_(['SUPER ADMINISTRADOR', "ADMINISTRADOR", "ALMACEN"])).all()

        for rol in roles:
            rol.modulos.append(almacen_m)
            rol.modulos.append(descuento_m)
            rol.modulos.append(query_descuento)
            rol.modulos.append(insert_descuento)
            rol.modulos.append(update_descuento)
            rol.modulos.append(delete_descuento)

        session.commit()
