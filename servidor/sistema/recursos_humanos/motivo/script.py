from servidor.database.connection import transaction
from servidor.sistema.usuarios.usuario.model import Modulo
from servidor.sistema.usuarios.rol.model import Rol
from servidor.sistema.recursos_humanos.motivo.model import Motivo



def insertions():
    with transaction() as session:
        recursos_humanos_m = session.query(Modulo).filter(Modulo.nombre == 'recursos_humanos_mod').first()
        if recursos_humanos_m is None:
            recursos_humanos_m = Modulo(titulo='Recursos Humanos', nombre='recursos_humanos_mod',
                                        icono='business_center')

        motivo_m = session.query(Modulo).filter(Modulo.nombre == 'motivo').first()
        if motivo_m is None:
            motivo_m = Modulo(titulo='Motivos', ruta='/motivo', nombre='motivo', icono='business')

        recursos_humanos_m.children.append(motivo_m)

        query_motivo = session.query(Modulo).filter(Modulo.nombre == 'motivo_query').first()
        if query_motivo is None:
            query_motivo = Modulo(titulo='Consultar', ruta='', nombre='motivo_query', menu=False)
        insert_motivo = session.query(Modulo).filter(Modulo.nombre == 'motivo_insert').first()
        if insert_motivo is None:
            insert_motivo = Modulo(titulo='Adicionar', ruta='/motivo_insert', nombre='motivo_insert', menu=False)
        update_motivo = session.query(Modulo).filter(Modulo.nombre == 'motivo_update').first()
        if update_motivo is None:
            update_motivo = Modulo(titulo='Actualizar', ruta='/motivo_update', nombre='motivo_update', menu=False)
        delete_motivo = session.query(Modulo).filter(Modulo.nombre == 'motivo_delete').first()
        if delete_motivo is None:
            delete_motivo = Modulo(titulo='Dar de Baja', ruta='/motivo_delete', nombre='motivo_delete', menu=False)

        motivo_m.children.append(query_motivo)
        motivo_m.children.append(insert_motivo)
        motivo_m.children.append(update_motivo)
        motivo_m.children.append(delete_motivo)

        roles = session.query(Rol).filter(Rol.nombre.in_(['SUPER ADMINISTRADOR', "ADMINISTRADOR", "RRHH"])).all()

        for rol in roles:
            rol.modulos.append(recursos_humanos_m)
            rol.modulos.append(motivo_m)
            rol.modulos.append(query_motivo)
            rol.modulos.append(insert_motivo)
            rol.modulos.append(update_motivo)
            rol.modulos.append(delete_motivo)

        session.add(Motivo(nombre='Dotacion',tipo="Descuento",monto=0))
        session.add(Motivo(nombre='Daño ',tipo="Descuento",monto=0))
        session.add(Motivo(nombre='Perdida',tipo="Descuento",monto=0))


        session.commit()
