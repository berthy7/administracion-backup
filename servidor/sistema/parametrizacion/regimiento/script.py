from servidor.database.connection import transaction
from servidor.sistema.usuarios.usuario.model import Modulo
from servidor.sistema.usuarios.rol.model import Rol
from servidor.sistema.parametrizacion.regimiento.model import Regimiento


def insertions():
    with transaction() as session:
        parametrizacion_m = session.query(Modulo).filter(Modulo.nombre == 'parametrizacion_mod').first()
        if parametrizacion_m is None:
            parametrizacion_m = Modulo(titulo='Parametrizacion', nombre='parametrizacion_mod', icono='business_center')

        regimiento_m = session.query(Modulo).filter(Modulo.nombre == 'regimiento').first()
        if regimiento_m is None:
            regimiento_m = Modulo(titulo='Regimientos militares', ruta='/regimiento', nombre='regimiento', icono='business')

        parametrizacion_m.children.append(regimiento_m)

        query_regimiento = session.query(Modulo).filter(Modulo.nombre == 'regimiento_query').first()
        if query_regimiento is None:
            query_regimiento = Modulo(titulo='Consultar', ruta='', nombre='regimiento_query', menu=False)
        insert_regimiento = session.query(Modulo).filter(Modulo.nombre == 'regimiento_insert').first()
        if insert_regimiento is None:
            insert_regimiento = Modulo(titulo='Adicionar', ruta='/regimiento_insert', nombre='regimiento_insert', menu=False)
        update_regimiento = session.query(Modulo).filter(Modulo.nombre == 'regimiento_update').first()
        if update_regimiento is None:
            update_regimiento = Modulo(titulo='Actualizar', ruta='/regimiento_update', nombre='regimiento_update', menu=False)
        delete_regimiento = session.query(Modulo).filter(Modulo.nombre == 'regimiento_delete').first()
        if delete_regimiento is None:
            delete_regimiento = Modulo(titulo='Dar de Baja', ruta='/regimiento_delete', nombre='regimiento_delete', menu=False)

        regimiento_m.children.append(query_regimiento)
        regimiento_m.children.append(insert_regimiento)
        regimiento_m.children.append(update_regimiento)
        regimiento_m.children.append(delete_regimiento)

        roles = session.query(Rol).filter(Rol.nombre.in_(['SUPER ADMINISTRADOR', "ADMINISTRADOR"])).all()

        for rol in roles:
            rol.modulos.append(parametrizacion_m)
            rol.modulos.append(regimiento_m)
            rol.modulos.append(query_regimiento)
            rol.modulos.append(insert_regimiento)
            rol.modulos.append(update_regimiento)
            rol.modulos.append(delete_regimiento)

        session.add(Regimiento(nombre='BATALLON LOGISTICO'))

        session.commit()
