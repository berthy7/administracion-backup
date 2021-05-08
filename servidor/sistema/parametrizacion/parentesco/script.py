from servidor.database.connection import transaction
from servidor.sistema.usuarios.usuario.model import Modulo
from servidor.sistema.usuarios.rol.model import Rol
from servidor.sistema.parametrizacion.parentesco.model import Parentesco


def insertions():
    with transaction() as session:
        parametrizacion_m = session.query(Modulo).filter(Modulo.nombre == 'parametrizacion_mod').first()
        if parametrizacion_m is None:
            parametrizacion_m = Modulo(titulo='Parametrizacion', nombre='parametrizacion_mod', icono='business_center')

        parentesco_m = session.query(Modulo).filter(Modulo.nombre == 'parentesco').first()
        if parentesco_m is None:
            parentesco_m = Modulo(titulo='Parentesco', ruta='/parentesco', nombre='parentesco', icono='business')

        parametrizacion_m.children.append(parentesco_m)

        query_parentesco = session.query(Modulo).filter(Modulo.nombre == 'parentesco_query').first()
        if query_parentesco is None:
            query_parentesco = Modulo(titulo='Consultar', ruta='', nombre='parentesco_query', menu=False)
        insert_parentesco = session.query(Modulo).filter(Modulo.nombre == 'parentesco_insert').first()
        if insert_parentesco is None:
            insert_parentesco = Modulo(titulo='Adicionar', ruta='/parentesco_insert', nombre='parentesco_insert', menu=False)
        update_parentesco = session.query(Modulo).filter(Modulo.nombre == 'parentesco_update').first()
        if update_parentesco is None:
            update_parentesco = Modulo(titulo='Actualizar', ruta='/parentesco_update', nombre='parentesco_update', menu=False)
        delete_parentesco = session.query(Modulo).filter(Modulo.nombre == 'parentesco_delete').first()
        if delete_parentesco is None:
            delete_parentesco = Modulo(titulo='Dar de Baja', ruta='/parentesco_delete', nombre='parentesco_delete', menu=False)

        parentesco_m.children.append(query_parentesco)
        parentesco_m.children.append(insert_parentesco)
        parentesco_m.children.append(update_parentesco)
        parentesco_m.children.append(delete_parentesco)

        roles = session.query(Rol).filter(Rol.nombre.in_(['SUPER ADMINISTRADOR', "ADMINISTRADOR"])).all()

        for rol in roles:
            rol.modulos.append(parametrizacion_m)
            rol.modulos.append(parentesco_m)
            rol.modulos.append(query_parentesco)
            rol.modulos.append(insert_parentesco)
            rol.modulos.append(update_parentesco)
            rol.modulos.append(delete_parentesco)

        session.add(Parentesco(nombre='Esposa'))
        session.add(Parentesco(nombre='Padre'))
        session.add(Parentesco(nombre='Madre'))

        session.commit()
