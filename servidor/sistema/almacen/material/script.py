from servidor.database.connection import transaction
from servidor.sistema.usuarios.usuario.model import Modulo
from servidor.sistema.usuarios.rol.model import Rol
from servidor.sistema.almacen.material.model import MaterialTipo,MaterialColor,MaterialTalla



def insertions():
    with transaction() as session:
        almacen_m = session.query(Modulo).filter(Modulo.nombre == 'almacen_mod').first()
        if almacen_m is None:
            almacen_m = Modulo(titulo='Almacen', nombre='almacen_mod', icono='business_center')

        material_m = session.query(Modulo).filter(Modulo.nombre == 'material').first()
        if material_m is None:
            material_m = Modulo(titulo='Material', ruta='/material', nombre='material', icono='business')

        almacen_m.children.append(material_m)

        query_material = session.query(Modulo).filter(Modulo.nombre == 'material_query').first()
        if query_material is None:
            query_material = Modulo(titulo='Consultar', ruta='', nombre='material_query', menu=False)
        insert_material = session.query(Modulo).filter(Modulo.nombre == 'material_insert').first()
        if insert_material is None:
            insert_material = Modulo(titulo='Adicionar', ruta='/material_insert', nombre='material_insert', menu=False)
        update_material = session.query(Modulo).filter(Modulo.nombre == 'material_update').first()
        if update_material is None:
            update_material = Modulo(titulo='Actualizar', ruta='/material_update', nombre='material_update', menu=False)
        delete_material = session.query(Modulo).filter(Modulo.nombre == 'material_delete').first()
        if delete_material is None:
            delete_material = Modulo(titulo='Dar de Baja', ruta='/material_delete', nombre='material_delete', menu=False)

        material_m.children.append(query_material)
        material_m.children.append(insert_material)
        material_m.children.append(update_material)
        material_m.children.append(delete_material)

        roles = session.query(Rol).filter(Rol.nombre.in_(['SUPER ADMINISTRADOR', "ADMINISTRADOR", "ALMACEN"])).all()

        for rol in roles:
            rol.modulos.append(almacen_m)
            rol.modulos.append(material_m)
            rol.modulos.append(query_material)
            rol.modulos.append(insert_material)
            rol.modulos.append(update_material)
            rol.modulos.append(delete_material)

        session.add(MaterialTipo(nombre='Uniforme'))

        session.add(MaterialTalla(nombre='P'))
        session.add(MaterialTalla(nombre='M'))
        session.add(MaterialTalla(nombre='L'))
        session.add(MaterialTalla(nombre='G'))
        session.add(MaterialTalla(nombre='XL'))
        session.add(MaterialTalla(nombre='XXL'))
        session.add(MaterialTalla(nombre='XXL'))
        session.add(MaterialTalla(nombre='29'))
        session.add(MaterialTalla(nombre='30'))
        session.add(MaterialTalla(nombre='31'))
        session.add(MaterialTalla(nombre='32'))
        session.add(MaterialTalla(nombre='33'))
        session.add(MaterialTalla(nombre='34'))
        session.add(MaterialTalla(nombre='35'))
        session.add(MaterialTalla(nombre='36'))
        session.add(MaterialTalla(nombre='37'))
        session.add(MaterialTalla(nombre='38'))
        session.add(MaterialTalla(nombre='39'))
        session.add(MaterialTalla(nombre='40'))
        session.add(MaterialTalla(nombre='41'))
        session.add(MaterialTalla(nombre='42'))
        session.add(MaterialTalla(nombre='43'))
        session.add(MaterialTalla(nombre='44'))
        session.add(MaterialTalla(nombre='45'))
        session.add(MaterialTalla(nombre='46'))
        session.add(MaterialTalla(nombre='47'))
        session.add(MaterialTalla(nombre='48'))
        session.add(MaterialTalla(nombre='49'))
        session.add(MaterialTalla(nombre='50'))

        session.add(MaterialColor(nombre='AMARILLO'))
        session.add(MaterialColor(nombre='AZUL'))
        session.add(MaterialColor(nombre='BLANCO'))
        session.add(MaterialColor(nombre='CAFE'))
        session.add(MaterialColor(nombre='CELESTE'))
        session.add(MaterialColor(nombre='COBRE'))
        session.add(MaterialColor(nombre='GRIS'))
        session.add(MaterialColor(nombre='NARANJA'))
        session.add(MaterialColor(nombre='NEGRO'))
        session.add(MaterialColor(nombre='PLATEADO'))
        session.add(MaterialColor(nombre='PLOMO'))
        session.add(MaterialColor(nombre='ROJO'))
        session.add(MaterialColor(nombre='ROSADO'))
        session.add(MaterialColor(nombre='VERDE'))
        session.add(MaterialColor(nombre='PLATA'))

        session.commit()
