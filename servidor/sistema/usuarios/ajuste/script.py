from servidor.database.connection import transaction
from servidor.sistema.usuarios.usuario.model import Modulo
from servidor.sistema.usuarios.rol.model import Rol
from servidor.sistema.usuarios.ajuste.model import Ajuste


def insertions():
    with transaction() as session:
        user_m = session.query(Modulo).filter(Modulo.nombre == 'usuarios_mod').first()
        if user_m is None:
            user_m = Modulo(titulo='Usuarios', nombre='usuarios_mod', icono='group')

        ajustes_m = session.query(Modulo).filter(Modulo.nombre == 'ajuste').first()
        if ajustes_m is None:
            ajustes_m = Modulo(titulo='Ajuste', ruta='/ajuste', nombre='ajuste', icono='settings')

        user_m.children.append(ajustes_m)

        query_ajuste = session.query(Modulo).filter(Modulo.nombre == 'rol_query').first()
        if query_ajuste is None:
            query_ajuste = Modulo(titulo='Consultar', ruta='', nombre='ajuste_query', menu=False)
        insert_ajuste = session.query(Modulo).filter(Modulo.nombre == 'ajuste_insert').first()
        if insert_ajuste is None:
            insert_ajuste = Modulo(titulo='Adicionar', ruta='/ajuste_insert', nombre='ajuste_insert', menu=False)
        update_ajuste = session.query(Modulo).filter(Modulo.nombre == 'ajuste_update').first()
        if update_ajuste is None:
            update_ajuste = Modulo(titulo='Actualizar', ruta='/ajuste_update', nombre='ajuste_update', menu=False)
        delete_ajuste = session.query(Modulo).filter(Modulo.nombre == 'ajuste_delete').first()
        if delete_ajuste is None:
            delete_ajuste = Modulo(titulo='Dar de Baja', ruta='/ajuste_delete', nombre='ajuste_delete', menu=False)

        ajustes_m.children.append(query_ajuste)
        ajustes_m.children.append(insert_ajuste)
        ajustes_m.children.append(update_ajuste)
        ajustes_m.children.append(delete_ajuste)

        super_role = session.query(Rol).filter(Rol.nombre == 'SUPER ADMINISTRADOR').first()
        if super_role is None:
            super_role = Rol(nombre='SUPER ADMINISTRADOR', descripcion='Todos los permisos.')

        admin_role = session.query(Rol).filter(Rol.nombre == 'ADMINISTRADOR').first()
        if admin_role is None:
            admin_role = Rol(nombre='ADMINISTRADOR', descripcion='Solo permisos de administrador.')

        super_role.modulos.append(user_m)
        super_role.modulos.append(ajustes_m)
        super_role.modulos.append(query_ajuste)
        super_role.modulos.append(insert_ajuste)
        super_role.modulos.append(update_ajuste)
        super_role.modulos.append(delete_ajuste)

        session.add(super_role)
        session.add(admin_role)
        session.add(Ajuste(id=1, claveSecreta='SecretBackup'))

        session.commit()
