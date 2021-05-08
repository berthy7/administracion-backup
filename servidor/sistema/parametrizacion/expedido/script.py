from servidor.database.connection import transaction
from servidor.sistema.usuarios.usuario.model import Modulo
from servidor.sistema.usuarios.rol.model import Rol
from servidor.sistema.parametrizacion.expedido.model import Expedido


def insertions():
    with transaction() as session:
        parametrizacion_m = session.query(Modulo).filter(Modulo.nombre == 'parametrizacion_mod').first()
        if parametrizacion_m is None:
            parametrizacion_m = Modulo(titulo='Parametrizacion', nombre='parametrizacion_mod', icono='business_center')

        expedido_m = session.query(Modulo).filter(Modulo.nombre == 'expedido').first()
        if expedido_m is None:
            expedido_m = Modulo(titulo='Expedido', ruta='/expedido', nombre='expedido', icono='business')

        parametrizacion_m.children.append(expedido_m)

        query_expedido = session.query(Modulo).filter(Modulo.nombre == 'expedido_query').first()
        if query_expedido is None:
            query_expedido = Modulo(titulo='Consultar', ruta='', nombre='expedido_query', menu=False)
        insert_expedido = session.query(Modulo).filter(Modulo.nombre == 'expedido_insert').first()
        if insert_expedido is None:
            insert_expedido = Modulo(titulo='Adicionar', ruta='/expedido_insert', nombre='expedido_insert', menu=False)
        update_expedido = session.query(Modulo).filter(Modulo.nombre == 'expedido_update').first()
        if update_expedido is None:
            update_expedido = Modulo(titulo='Actualizar', ruta='/expedido_update', nombre='expedido_update', menu=False)
        delete_expedido = session.query(Modulo).filter(Modulo.nombre == 'expedido_delete').first()
        if delete_expedido is None:
            delete_expedido = Modulo(titulo='Dar de Baja', ruta='/expedido_delete', nombre='expedido_delete', menu=False)

        expedido_m.children.append(query_expedido)
        expedido_m.children.append(insert_expedido)
        expedido_m.children.append(update_expedido)
        expedido_m.children.append(delete_expedido)

        roles = session.query(Rol).filter(Rol.nombre.in_(['SUPER ADMINISTRADOR', "ADMINISTRADOR"])).all()

        for rol in roles:
            rol.modulos.append(parametrizacion_m)
            rol.modulos.append(expedido_m)
            rol.modulos.append(query_expedido)
            rol.modulos.append(insert_expedido)
            rol.modulos.append(update_expedido)
            rol.modulos.append(delete_expedido)

        session.add(Expedido(nombre='Beni'))
        session.add(Expedido( nombre='Chuquisaca'))
        session.add(Expedido(nombre='Cochabamba'))
        session.add(Expedido(nombre='La Paz'))
        session.add(Expedido(nombre='Oruro'))
        session.add(Expedido(nombre='Pando'))
        session.add(Expedido(nombre='Potosi'))
        session.add(Expedido(nombre='Santa Cruz'))
        session.add(Expedido(nombre='Tarija'))

        session.commit()
