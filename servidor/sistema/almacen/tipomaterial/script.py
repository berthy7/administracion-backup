from servidor.database.connection import transaction
from servidor.sistema.usuarios.usuario.model import Modulo
from servidor.sistema.usuarios.rol.model import Rol



def insertions():
    with transaction() as session:
        almacen_m = session.query(Modulo).filter(Modulo.nombre == 'almacen_mod').first()
        if almacen_m is None:
            almacen_m = Modulo(titulo='Almacen', nombre='almacen_mod', icono='business_center')

        tipomaterial_m = session.query(Modulo).filter(Modulo.nombre == 'tipomaterial').first()
        if tipomaterial_m is None:
            tipomaterial_m = Modulo(titulo='Tipo Material', ruta='/tipomaterial', nombre='tipomaterial', icono='business')

        almacen_m.children.append(tipomaterial_m)

        query_tipomaterial = session.query(Modulo).filter(Modulo.nombre == 'tipomaterial_query').first()
        if query_tipomaterial is None:
            query_tipomaterial = Modulo(titulo='Consultar', ruta='', nombre='tipomaterial_query', menu=False)
        insert_tipomaterial = session.query(Modulo).filter(Modulo.nombre == 'tipomaterial_insert').first()
        if insert_tipomaterial is None:
            insert_tipomaterial = Modulo(titulo='Adicionar', ruta='/tipomaterial_insert', nombre='tipomaterial_insert', menu=False)
        update_tipomaterial = session.query(Modulo).filter(Modulo.nombre == 'tipomaterial_update').first()
        if update_tipomaterial is None:
            update_tipomaterial = Modulo(titulo='Actualizar', ruta='/tipomaterial_update', nombre='tipomaterial_update', menu=False)
        delete_tipomaterial = session.query(Modulo).filter(Modulo.nombre == 'tipomaterial_delete').first()
        if delete_tipomaterial is None:
            delete_tipomaterial = Modulo(titulo='Dar de Baja', ruta='/tipomaterial_delete', nombre='tipomaterial_delete', menu=False)

        tipomaterial_m.children.append(query_tipomaterial)
        tipomaterial_m.children.append(insert_tipomaterial)
        tipomaterial_m.children.append(update_tipomaterial)
        tipomaterial_m.children.append(delete_tipomaterial)

        roles = session.query(Rol).filter(Rol.nombre.in_(['SUPER ADMINISTRADOR', "ADMINISTRADOR", "ALMACEN"])).all()

        for rol in roles:
            rol.modulos.append(almacen_m)
            rol.modulos.append(tipomaterial_m)
            rol.modulos.append(query_tipomaterial)
            rol.modulos.append(insert_tipomaterial)
            rol.modulos.append(update_tipomaterial)
            rol.modulos.append(delete_tipomaterial)

        session.commit()
