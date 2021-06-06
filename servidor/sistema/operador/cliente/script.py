from servidor.database.connection import transaction
from servidor.sistema.usuarios.usuario.model import Modulo
from servidor.sistema.usuarios.rol.model import Rol
from servidor.sistema.operador.cliente.model import Cliente




def insertions():
    with transaction() as session:
        operador_m = session.query(Modulo).filter(Modulo.nombre == 'operador_mod').first()
        if operador_m is None:
            operador_m = Modulo(titulo='Operador', nombre='operador_mod', icono='business_center')

        cliente_m = session.query(Modulo).filter(Modulo.nombre == 'cliente').first()
        if cliente_m is None:
            cliente_m = Modulo(titulo='Cliente', ruta='/cliente', nombre='cliente', icono='business')

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


        session.add(Cliente(nombre='BACKUP',dia="BCK",noche="BCK-N"))
        session.add(Cliente(nombre='CONSTRUCTORA GOMEZ',dia="COG",noche="COG-N"))
        session.add(Cliente(nombre='IFA BANZER',dia="IFZ",noche="IFZ-N"))
        session.add(Cliente(nombre='IFA BENI',dia="IFB",noche="IFB-N"))
        session.add(Cliente(nombre='IFA BANZER ALMACEN',dia="IFM",noche="IFM-N"))
        session.add(Cliente(nombre='NELLY 1',dia="NL1",noche="NL1-N"))
        session.add(Cliente(nombre='NELLY 2',dia="NL2",noche="NL2-N"))
        session.add(Cliente(nombre='AVESCA',dia="AVE",noche="AVE-N"))
        session.add(Cliente(nombre='DOMICILIO SR.ROCA',dia="RDM",noche="RDM-N"))
        session.add(Cliente(nombre='URUBO GARDEN',dia="URG",noche="URG-N"))
        session.add(Cliente(nombre='LA FLORESTA',dia="FLO",noche="FLO-N"))
        session.add(Cliente(nombre='PRAXI 1', dia="PX1", noche="PX1-N"))
        session.add(Cliente(nombre='PRAXI 2', dia="PX2", noche="PX2-N"))
        session.add(Cliente(nombre='BARRIO NORTE', dia="BNO", noche="BNO-N"))
        session.add(Cliente(nombre='CIUDAD JARDIN', dia="CJA", noche="CJA-N"))
        session.add(Cliente(nombre='BARCELO', dia="BAC", noche="BAC-N"))
        session.add(Cliente(nombre='LAS PALMAS II', dia="PL2", noche="PL2-N"))
        session.add(Cliente(nombre='4LIVE', dia="LIV", noche="LIV-N"))
        session.add(Cliente(nombre='LA RIVIERA', dia="RIV", noche="RIV-N"))
        session.add(Cliente(nombre='CUBO II', dia="CUB", noche="CUB-N"))
        session.add(Cliente(nombre='SAE', dia="SAE", noche="SAE-N"))
        session.add(Cliente(nombre='IGUAZU', dia="IGU", noche="IGU-N"))
        session.add(Cliente(nombre='DATEC', dia="DTC", noche="DTC-N"))
        session.add(Cliente(nombre='PUESTO NUEVO 1', dia="PN1", noche="PN1-N"))
        session.add(Cliente(nombre='PUESTO NUEVO 2', dia="PN2", noche="PN2-N"))
        session.add(Cliente(nombre='PUESTO NUEVO 3', dia="PN3", noche="PN3-N"))
        session.add(Cliente(nombre='PUESTO NUEVO 4', dia="PN4", noche="PN4-N"))

        session.commit()
