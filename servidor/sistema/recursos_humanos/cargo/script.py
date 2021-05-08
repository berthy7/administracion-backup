from servidor.database.connection import transaction
from servidor.sistema.usuarios.usuario.model import Modulo
from servidor.sistema.usuarios.rol.model import Rol
from servidor.sistema.recursos_humanos.cargo.model import Cargo



def insertions():
    with transaction() as session:
        recursos_humanos_m = session.query(Modulo).filter(Modulo.nombre == 'recursos_humanos_mod').first()
        if recursos_humanos_m is None:
            recursos_humanos_m = Modulo(titulo='Recursos Humanos', nombre='recursos_humanos_mod',
                                        icono='business_center')

        cargo_m = session.query(Modulo).filter(Modulo.nombre == 'cargo').first()
        if cargo_m is None:
            cargo_m = Modulo(titulo='Cargo', ruta='/cargo', nombre='cargo', icono='business')

        recursos_humanos_m.children.append(cargo_m)

        query_cargo = session.query(Modulo).filter(Modulo.nombre == 'cargo_query').first()
        if query_cargo is None:
            query_cargo = Modulo(titulo='Consultar', ruta='', nombre='cargo_query', menu=False)
        insert_cargo = session.query(Modulo).filter(Modulo.nombre == 'cargo_insert').first()
        if insert_cargo is None:
            insert_cargo = Modulo(titulo='Adicionar', ruta='/cargo_insert', nombre='cargo_insert', menu=False)
        update_cargo = session.query(Modulo).filter(Modulo.nombre == 'cargo_update').first()
        if update_cargo is None:
            update_cargo = Modulo(titulo='Actualizar', ruta='/cargo_update', nombre='cargo_update', menu=False)
        delete_cargo = session.query(Modulo).filter(Modulo.nombre == 'cargo_delete').first()
        if delete_cargo is None:
            delete_cargo = Modulo(titulo='Dar de Baja', ruta='/cargo_delete', nombre='cargo_delete', menu=False)

        cargo_m.children.append(query_cargo)
        cargo_m.children.append(insert_cargo)
        cargo_m.children.append(update_cargo)
        cargo_m.children.append(delete_cargo)

        roles = session.query(Rol).filter(Rol.nombre.in_(['SUPER ADMINISTRADOR', "ADMINISTRADOR"])).all()

        for rol in roles:
            rol.modulos.append(recursos_humanos_m)
            rol.modulos.append(cargo_m)
            rol.modulos.append(query_cargo)
            rol.modulos.append(insert_cargo)
            rol.modulos.append(update_cargo)
            rol.modulos.append(delete_cargo)

        session.add(Cargo(nombre='GUARDIA DE SEGURIDAD'))
        session.add(Cargo(nombre='SUPERVISOR'))
        session.add(Cargo(nombre='JEFE DE OPERACIONES'))
        session.add(Cargo(nombre='INFORMACIONES'))
        session.add(Cargo(nombre='OPERADOR'))
        session.add(Cargo(nombre='ALMACEN'))
        session.add(Cargo(nombre='SISTEMAS'))
        session.add(Cargo(nombre='LIMPIEZA'))
        session.add(Cargo(nombre='RECEPCION'))
        session.add(Cargo(nombre='RECURSOS HUMANOS'))
        session.add(Cargo(nombre='GERENTE ADMINISTRATIVO'))
        session.add(Cargo(nombre='GERENTE GENERAL'))
        session.add(Cargo(nombre='IMÁGENES'))
        session.add(Cargo(nombre='AUXILIAR ADMINISTRATIVO'))
        session.add(Cargo(nombre='CHOFER'))
        session.add(Cargo(nombre='AUXILIAR CONTABLE'))
        session.add(Cargo(nombre='PASANTE'))
        session.add(Cargo(nombre='AUXILIAR DE SISTEMA'))

        session.commit()
