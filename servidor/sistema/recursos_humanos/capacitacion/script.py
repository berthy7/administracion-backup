from servidor.database.connection import transaction
from servidor.sistema.usuarios.usuario.model import Modulo
from servidor.sistema.usuarios.rol.model import Rol
from servidor.sistema.recursos_humanos.capacitacion.manager import Titulo,Tema



def insertions():
    with transaction() as session:
        recursos_humanos_m = session.query(Modulo).filter(Modulo.nombre == 'recursos_humanos_mod').first()
        if recursos_humanos_m is None:
            recursos_humanos_m = Modulo(titulo='Recursos Humanos', nombre='recursos_humanos_mod',
                                        icono='business_center')

        capacitacion_m = session.query(Modulo).filter(Modulo.nombre == 'capacitacion').first()
        if capacitacion_m is None:
            capacitacion_m = Modulo(titulo='Capacitaciones', ruta='/capacitacion', nombre='capacitacion', icono='business')

        recursos_humanos_m.children.append(capacitacion_m)

        query_capacitacion = session.query(Modulo).filter(Modulo.nombre == 'capacitacion_query').first()
        if query_capacitacion is None:
            query_capacitacion = Modulo(titulo='Consultar', ruta='', nombre='capacitacion_query', menu=False)
        insert_capacitacion = session.query(Modulo).filter(Modulo.nombre == 'capacitacion_insert').first()
        if insert_capacitacion is None:
            insert_capacitacion = Modulo(titulo='Adicionar', ruta='/capacitacion_insert', nombre='capacitacion_insert', menu=False)
        update_capacitacion = session.query(Modulo).filter(Modulo.nombre == 'capacitacion_update').first()
        if update_capacitacion is None:
            update_capacitacion = Modulo(titulo='Actualizar', ruta='/capacitacion_update', nombre='capacitacion_update', menu=False)
        delete_capacitacion = session.query(Modulo).filter(Modulo.nombre == 'capacitacion_delete').first()
        if delete_capacitacion is None:
            delete_capacitacion = Modulo(titulo='Dar de Baja', ruta='/capacitacion_delete', nombre='capacitacion_delete', menu=False)

        capacitacion_m.children.append(query_capacitacion)
        capacitacion_m.children.append(insert_capacitacion)
        capacitacion_m.children.append(update_capacitacion)
        capacitacion_m.children.append(delete_capacitacion)

        roles = session.query(Rol).filter(Rol.nombre.in_(['SUPER ADMINISTRADOR', "ADMINISTRADOR", "RRHH"])).all()

        for rol in roles:
            rol.modulos.append(recursos_humanos_m)
            rol.modulos.append(capacitacion_m)
            rol.modulos.append(query_capacitacion)
            rol.modulos.append(insert_capacitacion)
            rol.modulos.append(update_capacitacion)
            rol.modulos.append(delete_capacitacion)


        session.add(Titulo(nombre='Capacitacion Inicial'))
        session.add(Titulo(nombre='Capacitacion Recurrente'))
        session.add(Titulo(nombre='Capacitacion Especial'))

        session.add(Tema(nombre='Principios Basicos de un Guardia de Seguridad'))
        session.add(Tema(nombre='Procedimientos Generales de Seguridad'))
        session.add(Tema(nombre='Soporte Vital Basico'))
        session.add(Tema(nombre='Prevencion y Extincion de Incendios'))
        session.add(Tema(nombre='Procedimientos Especificos de Puestos'))

        session.commit()
