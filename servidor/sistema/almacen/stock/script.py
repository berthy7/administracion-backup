from servidor.database.connection import transaction
from servidor.sistema.usuarios.usuario.model import Modulo
from servidor.sistema.usuarios.rol.model import Rol



def insertions():
    with transaction() as session:
        almacen_m = session.query(Modulo).filter(Modulo.nombre == 'almacen_mod').first()
        if almacen_m is None:
            almacen_m = Modulo(titulo='Almacen', nombre='almacen_mod', icono='business_center')

        stock_m = session.query(Modulo).filter(Modulo.nombre == 'stock').first()
        if stock_m is None:
            stock_m = Modulo(titulo='Ingreso de Stock', ruta='/stock', nombre='stock', icono='business')

        almacen_m.children.append(stock_m)

        query_stock = session.query(Modulo).filter(Modulo.nombre == 'stock_query').first()
        if query_stock is None:
            query_stock = Modulo(titulo='Consultar', ruta='', nombre='stock_query', menu=False)
        insert_stock = session.query(Modulo).filter(Modulo.nombre == 'stock_insert').first()
        if insert_stock is None:
            insert_stock = Modulo(titulo='Adicionar', ruta='/stock_insert', nombre='stock_insert', menu=False)
        update_stock = session.query(Modulo).filter(Modulo.nombre == 'stock_update').first()
        if update_stock is None:
            update_stock = Modulo(titulo='Actualizar', ruta='/stock_update', nombre='stock_update', menu=False)
        delete_stock = session.query(Modulo).filter(Modulo.nombre == 'stock_delete').first()
        if delete_stock is None:
            delete_stock = Modulo(titulo='Dar de Baja', ruta='/stock_delete', nombre='stock_delete', menu=False)

        stock_m.children.append(query_stock)
        stock_m.children.append(insert_stock)
        stock_m.children.append(update_stock)
        stock_m.children.append(delete_stock)

        roles = session.query(Rol).filter(Rol.nombre.in_(['SUPER ADMINISTRADOR', "ADMINISTRADOR", "ALMACEN"])).all()

        for rol in roles:
            rol.modulos.append(almacen_m)
            rol.modulos.append(stock_m)
            rol.modulos.append(query_stock)
            rol.modulos.append(insert_stock)
            rol.modulos.append(update_stock)
            rol.modulos.append(delete_stock)

        session.commit()
