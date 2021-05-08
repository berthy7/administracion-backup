from servidor.database.connection import transaction
from servidor.sistema.usuarios.usuario.model import Modulo
from servidor.sistema.usuarios.rol.model import Rol
from servidor.sistema.parametrizacion.categoria.model import Categoria


def insertions():
    with transaction() as session:
        parametrizacion_m = session.query(Modulo).filter(Modulo.nombre == 'parametrizacion_mod').first()
        if parametrizacion_m is None:
            parametrizacion_m = Modulo(titulo='Parametrizacion', nombre='parametrizacion_mod', icono='business_center')

        categoria_m = session.query(Modulo).filter(Modulo.nombre == 'categoria').first()
        if categoria_m is None:
            categoria_m = Modulo(titulo='Categoria', ruta='/categoria', nombre='categoria', icono='business')

        parametrizacion_m.children.append(categoria_m)

        query_categoria = session.query(Modulo).filter(Modulo.nombre == 'categoria_query').first()
        if query_categoria is None:
            query_categoria = Modulo(titulo='Consultar', ruta='', nombre='categoria_query', menu=False)
        insert_categoria = session.query(Modulo).filter(Modulo.nombre == 'categoria_insert').first()
        if insert_categoria is None:
            insert_categoria = Modulo(titulo='Adicionar', ruta='/categoria_insert', nombre='categoria_insert', menu=False)
        update_categoria = session.query(Modulo).filter(Modulo.nombre == 'categoria_update').first()
        if update_categoria is None:
            update_categoria = Modulo(titulo='Actualizar', ruta='/categoria_update', nombre='categoria_update', menu=False)
        delete_categoria = session.query(Modulo).filter(Modulo.nombre == 'categoria_delete').first()
        if delete_categoria is None:
            delete_categoria = Modulo(titulo='Dar de Baja', ruta='/categoria_delete', nombre='categoria_delete', menu=False)

        categoria_m.children.append(query_categoria)
        categoria_m.children.append(insert_categoria)
        categoria_m.children.append(update_categoria)
        categoria_m.children.append(delete_categoria)

        roles = session.query(Rol).filter(Rol.nombre.in_(['SUPER ADMINISTRADOR', "ADMINISTRADOR"])).all()

        for rol in roles:
            rol.modulos.append(parametrizacion_m)
            rol.modulos.append(categoria_m)
            rol.modulos.append(query_categoria)
            rol.modulos.append(insert_categoria)
            rol.modulos.append(update_categoria)
            rol.modulos.append(delete_categoria)


        session.add(Categoria(nombre='A'))
        session.add(Categoria(nombre='B'))
        session.add(Categoria(nombre='C'))
        session.add(Categoria(nombre='P'))
        session.add(Categoria(nombre='M'))
        session.add(Categoria( nombre='T'))

        session.commit()
