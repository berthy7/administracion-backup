from servidor.database.connection import transaction
from servidor.sistema.usuarios.usuario.model import Modulo
from servidor.sistema.usuarios.rol.model import Rol
from servidor.sistema.parametrizacion.retiro.model import Retiro


def insertions():
    with transaction() as session:
        parametrizacion_m = session.query(Modulo).filter(Modulo.nombre == 'parametrizacion_mod').first()
        if parametrizacion_m is None:
            parametrizacion_m = Modulo(titulo='Parametrizacion', nombre='parametrizacion_mod', icono='business_center')

        retiro_m = session.query(Modulo).filter(Modulo.nombre == 'retiro').first()
        if retiro_m is None:
            retiro_m = Modulo(titulo='Retiro', ruta='/retiro', nombre='retiro', icono='business')

        parametrizacion_m.children.append(retiro_m)

        query_retiro = session.query(Modulo).filter(Modulo.nombre == 'retiro_query').first()
        if query_retiro is None:
            query_retiro = Modulo(titulo='Consultar', ruta='', nombre='retiro_query', menu=False)
        insert_retiro = session.query(Modulo).filter(Modulo.nombre == 'retiro_insert').first()
        if insert_retiro is None:
            insert_retiro = Modulo(titulo='Adicionar', ruta='/retiro_insert', nombre='retiro_insert', menu=False)
        update_retiro = session.query(Modulo).filter(Modulo.nombre == 'retiro_update').first()
        if update_retiro is None:
            update_retiro = Modulo(titulo='Actualizar', ruta='/retiro_update', nombre='retiro_update', menu=False)
        delete_retiro = session.query(Modulo).filter(Modulo.nombre == 'retiro_delete').first()
        if delete_retiro is None:
            delete_retiro = Modulo(titulo='Dar de Baja', ruta='/retiro_delete', nombre='retiro_delete', menu=False)

        retiro_m.children.append(query_retiro)
        retiro_m.children.append(insert_retiro)
        retiro_m.children.append(update_retiro)
        retiro_m.children.append(delete_retiro)

        roles = session.query(Rol).filter(Rol.nombre.in_(['SUPER ADMINISTRADOR', "ADMINISTRADOR"])).all()

        for rol in roles:
            rol.modulos.append(parametrizacion_m)
            rol.modulos.append(retiro_m)
            rol.modulos.append(query_retiro)
            rol.modulos.append(insert_retiro)
            rol.modulos.append(update_retiro)
            rol.modulos.append(delete_retiro)

        session.add(Retiro(nombre='Renuncia'))

        session.commit()
