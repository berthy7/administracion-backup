from servidor.database.connection import transaction
from servidor.sistema.usuarios.usuario.model import Modulo
from servidor.sistema.usuarios.rol.model import Rol
from servidor.sistema.operador.cliente.model import Cliente
from servidor.sistema.operador.asistencia.model import TipoAusencia,Turno




def insertions():
    with transaction() as session:
        operador_m = session.query(Modulo).filter(Modulo.nombre == 'operador_mod').first()
        if operador_m is None:
            operador_m = Modulo(titulo='Operador', nombre='operador_mod', icono='business_center')

        cliente_m = session.query(Modulo).filter(Modulo.nombre == 'cliente').first()
        if cliente_m is None:
            cliente_m = Modulo(titulo='Control de Asistencia', ruta='/cliente', nombre='cliente', icono='business')

        operador_m.children.append(cliente_m)

        query_cliente = session.query(Modulo).filter(Modulo.nombre == 'cliente_query').first()
        if query_cliente is None:
            query_cliente = Modulo(titulo='Consultar', ruta='', nombre='cliente_query', menu=False)
        insert_cliente = session.query(Modulo).filter(Modulo.nombre == 'cliente_insert').first()
        if insert_cliente is None:
            insert_cliente = Modulo(titulo='Adicionar', ruta='/cliente_insert', nombre='cliente_insert', menu=False)
        update_cliente = session.query(Modulo).filter(Modulo.nombre == 'cliente_update').first()
        if update_cliente is None:
            update_cliente = Modulo(titulo='Actualizar', ruta='/cliente_update', nombre='cliente_update', menu=False)
        delete_cliente = session.query(Modulo).filter(Modulo.nombre == 'cliente_delete').first()
        if delete_cliente is None:
            delete_cliente = Modulo(titulo='Dar de Baja', ruta='/cliente_delete', nombre='cliente_delete', menu=False)

        cliente_m.children.append(query_cliente)
        cliente_m.children.append(insert_cliente)
        cliente_m.children.append(update_cliente)
        cliente_m.children.append(delete_cliente)

        roles = session.query(Rol).filter(Rol.nombre.in_(['SUPER ADMINISTRADOR', "ADMINISTRADOR", "OPERADOR"])).all()

        for rol in roles:
            rol.modulos.append(operador_m)
            rol.modulos.append(cliente_m)
            rol.modulos.append(query_cliente)
            rol.modulos.append(insert_cliente)
            rol.modulos.append(update_cliente)
            rol.modulos.append(delete_cliente)


        session.add(Cliente(nombre='BACKUP',codigo="BCK"))
        session.add(Cliente(nombre='PUESTO MOVIL', codigo="MOV"))
        session.add(Cliente(nombre='CONSTRUCTORA GOMEZ',codigo="COG"))
        session.add(Cliente(nombre='IFA BANZER',codigo="IFZ"))
        session.add(Cliente(nombre='IFA BENI',codigo="IFB"))
        session.add(Cliente(nombre='IFA BANZER ALMACEN',codigo="IFM"))
        session.add(Cliente(nombre='NELLY 1',codigo="NL1"))
        session.add(Cliente(nombre='NELLY 2',codigo="NL2"))
        session.add(Cliente(nombre='AVESCA',codigo="AVE"))
        session.add(Cliente(nombre='DOMICILIO SR.ROCA',codigo="RDM"))
        session.add(Cliente(nombre='URUBO GARDEN',codigo="URG"))
        session.add(Cliente(nombre='LA FLORESTA',codigo="FLO"))
        session.add(Cliente(nombre='PRAXI 1', codigo="PX1"))
        session.add(Cliente(nombre='PRAXI 2', codigo="PX2"))
        session.add(Cliente(nombre='BARRIO NORTE', codigo="BNO"))
        session.add(Cliente(nombre='CIUDAD JARDIN', codigo="CJA"))
        session.add(Cliente(nombre='BARCELO', codigo="BAC"))
        session.add(Cliente(nombre='LAS PALMAS II', codigo="PL2"))
        session.add(Cliente(nombre='4LIVE', codigo="LIV"))
        session.add(Cliente(nombre='LA RIVIERA', codigo="RIV"))
        session.add(Cliente(nombre='CUBO II', codigo="CUB"))
        session.add(Cliente(nombre='SAE', codigo="SAE"))
        session.add(Cliente(nombre='IGUAZU', codigo="IGU"))
        session.add(Cliente(nombre='DATEC', codigo="DTC"))

        session.add(TipoAusencia(nombre='PRESENTE', codigo="PR", color="color_verde"))
        session.add(TipoAusencia(nombre='FALTA', codigo="F", color="color_rojo"))
        session.add(TipoAusencia(nombre='FRANCO',codigo="L", color="color_amarillo"))
        session.add(TipoAusencia(nombre='PERMISO',codigo="X", color="color_naranja"))
        session.add(TipoAusencia(nombre='BAJA MEDICA',codigo="BJM", color="color_cafe"))
        session.add(TipoAusencia(nombre='VACACION',codigo="V", color="color_rosado"))
        session.add(TipoAusencia(nombre='RETIRADOS',codigo="R", color="color_azul"))
        session.add(TipoAusencia(nombre='PERMISO SIN GOSE', codigo="PSG", color="color_celeste"))

        session.add(Turno(nombre='DIURNO'))
        session.add(Turno(nombre='NOCTURNO'))


        session.commit()
