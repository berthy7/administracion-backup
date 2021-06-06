from servidor.database.connection import transaction
from servidor.sistema.usuarios.usuario.model import Modulo
from servidor.sistema.usuarios.rol.model import Rol
from servidor.sistema.recursos_humanos.personal.model import TipoContrato


def insertions():
    with transaction() as session:
        recursos_humanos_m = session.query(Modulo).filter(Modulo.nombre == 'recursos_humanos_mod').first()
        if recursos_humanos_m is None:
            recursos_humanos_m = Modulo(titulo='Recursos Humanos', nombre='recursos_humanos_mod', icono='business_center')

        personal_m = session.query(Modulo).filter(Modulo.nombre == 'personal').first()
        if personal_m is None:
            personal_m = Modulo(titulo='Personal', ruta='/personal', nombre='personal', icono='business')

        recursos_humanos_m.children.append(personal_m)

        query_personal = session.query(Modulo).filter(Modulo.nombre == 'personal_query').first()
        if query_personal is None:
            query_personal = Modulo(titulo='Consultar', ruta='', nombre='personal_query', menu=False)
        insert_personal = session.query(Modulo).filter(Modulo.nombre == 'personal_insert').first()
        if insert_personal is None:
            insert_personal = Modulo(titulo='Adicionar', ruta='/personal_insert', nombre='personal_insert', menu=False)
        update_personal = session.query(Modulo).filter(Modulo.nombre == 'personal_update').first()
        if update_personal is None:
            update_personal = Modulo(titulo='Actualizar', ruta='/personal_update', nombre='personal_update', menu=False)
        delete_personal = session.query(Modulo).filter(Modulo.nombre == 'personal_delete').first()
        if delete_personal is None:
            delete_personal = Modulo(titulo='Dar de Baja', ruta='/personal_delete', nombre='personal_delete', menu=False)

        personal_m.children.append(query_personal)
        personal_m.children.append(insert_personal)
        personal_m.children.append(update_personal)
        personal_m.children.append(delete_personal)

        roles = session.query(Rol).filter(Rol.nombre.in_(['SUPER ADMINISTRADOR', "ADMINISTRADOR", "RRHH"])).all()

        for rol in roles:
            rol.modulos.append(recursos_humanos_m)
            rol.modulos.append(personal_m)
            rol.modulos.append(query_personal)
            rol.modulos.append(insert_personal)
            rol.modulos.append(update_personal)
            rol.modulos.append(delete_personal)

        session.add(TipoContrato(nombre='PLAZO FIJO'))
        session.add(TipoContrato(nombre='INDEFINIDO'))
        session.add(TipoContrato(nombre='PASANTE'))
        session.add(TipoContrato(nombre='CONSULTOR'))
        session.add(TipoContrato(nombre='POR PROYECTO'))

        session.commit()
