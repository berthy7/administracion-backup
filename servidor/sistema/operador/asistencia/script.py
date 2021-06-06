from servidor.database.connection import transaction
from servidor.sistema.usuarios.usuario.model import Modulo
from servidor.sistema.usuarios.rol.model import Rol
from servidor.sistema.operador.asistencia.model import TipoAusencia



def insertions():
    with transaction() as session:
        operador_m = session.query(Modulo).filter(Modulo.nombre == 'operador_mod').first()
        if operador_m is None:
            operador_m = Modulo(titulo='Operador', nombre='operador_mod', icono='business_center')

        asistencia_m = session.query(Modulo).filter(Modulo.nombre == 'asistencia').first()
        if asistencia_m is None:
            asistencia_m = Modulo(titulo='Asistencia', ruta='/asistencia', nombre='asistencia', icono='business')

        operador_m.children.append(asistencia_m)

        query_asistencia = session.query(Modulo).filter(Modulo.nombre == 'asistencia_query').first()
        if query_asistencia is None:
            query_asistencia = Modulo(titulo='Consultar', ruta='', nombre='asistencia_query', menu=False)
        insert_asistencia = session.query(Modulo).filter(Modulo.nombre == 'asistencia_insert').first()
        if insert_asistencia is None:
            insert_asistencia = Modulo(titulo='Adicionar', ruta='/asistencia_insert', nombre='asistencia_insert', menu=False)
        update_asistencia = session.query(Modulo).filter(Modulo.nombre == 'asistencia_update').first()
        if update_asistencia is None:
            update_asistencia = Modulo(titulo='Actualizar', ruta='/asistencia_update', nombre='asistencia_update', menu=False)
        delete_asistencia = session.query(Modulo).filter(Modulo.nombre == 'asistencia_delete').first()
        if delete_asistencia is None:
            delete_asistencia = Modulo(titulo='Dar de Baja', ruta='/asistencia_delete', nombre='asistencia_delete', menu=False)

        asistencia_m.children.append(query_asistencia)
        asistencia_m.children.append(insert_asistencia)
        asistencia_m.children.append(update_asistencia)
        asistencia_m.children.append(delete_asistencia)

        roles = session.query(Rol).filter(Rol.nombre.in_(['SUPER ADMINISTRADOR', "ADMINISTRADOR", "OPERADOR"])).all()

        for rol in roles:
            rol.modulos.append(operador_m)
            rol.modulos.append(asistencia_m)
            rol.modulos.append(query_asistencia)
            rol.modulos.append(insert_asistencia)
            rol.modulos.append(update_asistencia)
            rol.modulos.append(delete_asistencia)

        session.add(TipoAusencia(nombre='FRANCO',codigo="L"))
        session.add(TipoAusencia(nombre='FALTA',codigo="F"))
        session.add(TipoAusencia(nombre='PERMISO',codigo="X"))
        session.add(TipoAusencia(nombre='BAJA MEDICA',codigo="BJM"))
        session.add(TipoAusencia(nombre='VACACION',codigo="V"))
        session.add(TipoAusencia(nombre='RETIRADOS',codigo="R"))
        session.add(TipoAusencia(nombre='PERMISO SIN GOSE DE HABER', codigo="PSG"))

        session.commit()
