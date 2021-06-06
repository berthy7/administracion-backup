from servidor.database.connection import transaction
from servidor.sistema.usuarios.usuario.model import Modulo
from servidor.sistema.usuarios.rol.model import Rol


def insertions():
    with transaction() as session:
        operador_m = session.query(Modulo).filter(Modulo.nombre == 'operador_mod').first()
        if operador_m is None:
            operador_m = Modulo(titulo='Operador', nombre='operador_mod', icono='business_center')

        postulante_m = session.query(Modulo).filter(Modulo.nombre == 'postulante').first()
        if postulante_m is None:
            postulante_m = Modulo(titulo='Postulantes', ruta='/postulante', nombre='postulante', icono='business')

        operador_m.children.append(postulante_m)

        query_postulante = session.query(Modulo).filter(Modulo.nombre == 'postulante_query').first()
        if query_postulante is None:
            query_postulante = Modulo(titulo='Consultar', ruta='', nombre='postulante_query', menu=False)
        insert_postulante = session.query(Modulo).filter(Modulo.nombre == 'postulante_insert').first()
        if insert_postulante is None:
            insert_postulante = Modulo(titulo='Adicionar', ruta='/postulante_insert', nombre='postulante_insert', menu=False)
        update_postulante = session.query(Modulo).filter(Modulo.nombre == 'postulante_update').first()
        if update_postulante is None:
            update_postulante = Modulo(titulo='Actualizar', ruta='/postulante_update', nombre='postulante_update', menu=False)
        delete_postulante = session.query(Modulo).filter(Modulo.nombre == 'postulante_delete').first()
        if delete_postulante is None:
            delete_postulante = Modulo(titulo='Dar de Baja', ruta='/postulante_delete', nombre='postulante_delete', menu=False)

        postulante_m.children.append(query_postulante)
        postulante_m.children.append(insert_postulante)
        postulante_m.children.append(update_postulante)
        postulante_m.children.append(delete_postulante)

        roles = session.query(Rol).filter(Rol.nombre.in_(['SUPER ADMINISTRADOR', "ADMINISTRADOR", "OPERADOR"])).all()

        for rol in roles:
            rol.modulos.append(operador_m)
            rol.modulos.append(postulante_m)
            rol.modulos.append(query_postulante)
            rol.modulos.append(insert_postulante)
            rol.modulos.append(update_postulante)
            rol.modulos.append(delete_postulante)


        session.commit()
