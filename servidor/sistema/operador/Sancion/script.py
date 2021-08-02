from servidor.database.connection import transaction
from servidor.sistema.usuarios.usuario.model import Modulo
from servidor.sistema.usuarios.rol.model import Rol


def insertions():
    with transaction() as session:
        operador_m = session.query(Modulo).filter(Modulo.nombre == 'operador_mod').first()
        if operador_m is None:
            operador_m = Modulo(titulo='Operador', nombre='operador_mod', icono='business_center')

        sancion_m = session.query(Modulo).filter(Modulo.nombre == 'sancion').first()
        if sancion_m is None:
            sancion_m = Modulo(titulo='Sanciones', ruta='/sancion', nombre='sancion', icono='business')

        operador_m.children.append(sancion_m)

        query_sancion = session.query(Modulo).filter(Modulo.nombre == 'sancion_query').first()
        if query_sancion is None:
            query_sancion = Modulo(titulo='Consultar', ruta='', nombre='sancion_query', menu=False)
        insert_sancion = session.query(Modulo).filter(Modulo.nombre == 'sancion_insert').first()
        if insert_sancion is None:
            insert_sancion = Modulo(titulo='Adicionar', ruta='/sancion_insert', nombre='sancion_insert', menu=False)
        update_sancion = session.query(Modulo).filter(Modulo.nombre == 'sancion_update').first()
        if update_sancion is None:
            update_sancion = Modulo(titulo='Actualizar', ruta='/sancion_update', nombre='sancion_update', menu=False)
        delete_sancion = session.query(Modulo).filter(Modulo.nombre == 'sancion_delete').first()
        if delete_sancion is None:
            delete_sancion = Modulo(titulo='Dar de Baja', ruta='/sancion_delete', nombre='sancion_delete', menu=False)

        sancion_m.children.append(query_sancion)
        sancion_m.children.append(insert_sancion)
        sancion_m.children.append(update_sancion)
        sancion_m.children.append(delete_sancion)

        roles = session.query(Rol).filter(Rol.nombre.in_(['SUPER ADMINISTRADOR', "ADMINISTRADOR", "OPERADOR"])).all()

        for rol in roles:
            rol.modulos.append(operador_m)
            rol.modulos.append(sancion_m)
            rol.modulos.append(query_sancion)
            rol.modulos.append(insert_sancion)
            rol.modulos.append(update_sancion)
            rol.modulos.append(delete_sancion)


        session.commit()
