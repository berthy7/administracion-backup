from servidor.common.managers import SuperManager
from servidor.sistema.usuarios.bitacora.manager import BitacoraManager
from servidor.sistema.usuarios.usuario.manager import UsuarioManager
from servidor.sistema.usuarios.bitacora.model import Bitacora
from servidor.sistema.recursos_humanos.personal.model import Personal

from datetime import datetime

import pytz

global fecha_zona
fecha_zona = datetime.now(pytz.timezone('America/La_Paz'))


class PostulanteManager(SuperManager):

    def __init__(self, db):
        super().__init__(Personal, db)


    def listar_habilitados(self):
        return self.db.query(self.entity).filter(self.entity.estado).filter(self.entity.enabled).all()

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled).all()

    def list_all(self):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled))

    def get_all(self):
        items = self.db.query(self.entity).filter(self.entity.estado).filter(self.entity.enabled)
        return items

    def all_data(self, idu):
        privilegios = UsuarioManager(self.db).get_privileges(idu, '/postulante')
        datos = self.db.query(self.entity).filter(self.entity.enabled).all()
        list = []

        for item in datos:
            is_active = item.estado
            disable = 'disabled' if 'postulante_update' not in privilegios else ''
            estado = 'Activo' if is_active else 'Inactivo'
            check = 'checked' if is_active else ''
            delete = 'postulante_delete' in privilegios

            diccionario = item.get_dict()
            diccionario['estado'] = estado
            diccionario['check'] = check
            diccionario['disable'] = disable
            diccionario['delete'] = delete
            diccionario['fullname'] = item.fullname

            list.append(diccionario)

        return list

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()
        objeto.tipo = "Postulante"
        objeto.fechar = fecha

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registró postulante.", fecha=fecha, tabla="almacen_postulante", identificador=a.id)
        super().insert(b)
        return a

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modificó postulante.", fecha=fecha, tabla="almacen_postulante", identificador=a.id)
        super().insert(b)
        return a


    def update_x_stock(self, stock):
        postulanteActual = self.db.query(self.entity).filter(self.entity.id == stock.fkpostulante).first()

        postulanteActual.cantidad = int(postulanteActual.cantidad) + int(stock.cantidad)
        postulanteActual.talla = stock.talla.nombre
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(postulanteActual)
        b = Bitacora(fkusuario=stock.user, ip=stock.ip, accion="Modificó cantidad postulante.", fecha=fecha,
                     tabla="almacen_postulante", identificador=a.id)
        
        super().insert(b)
        return a

    def update_detalle(self, stockDetalle):

        for det in stockDetalle:

            postulanteDetalle = self.db.query(PostulanteDetalle).filter(PostulanteDetalle.id == det.fkpostulanteDetalle).first()


            if postulanteDetalle:
                postulanteDetalle.cantidad = int(postulanteDetalle.cantidad) + int(det.cantidad)
                super().update(postulanteDetalle)

        self.db.commit()


    def update_detalle_asignacion(self, asignacionDetalle):

        for det in asignacionDetalle:

            postulanteDetalle = self.db.query(PostulanteDetalle).filter(PostulanteDetalle.id == det.fkpostulanteDetalle).first()


            if postulanteDetalle:
                postulanteDetalle.cantidad = int(postulanteDetalle.cantidad) - int(det.cantidad)
                super().update(postulanteDetalle)

        self.db.commit()


    def state(self, id, estado, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        mensaje = "Habilitó postulante" if estado else "Deshabilitó postulante"
        x.estado = estado

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion=mensaje, fecha=fecha, tabla="almacen_postulante", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()
        return x

    def delete(self, id, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = False

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó postulante", fecha=fecha, tabla="almacen_postulante", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()



class PostulanteTipoManager(SuperManager):

    def __init__(self, db):
        super().__init__(PostulanteTipo, db)


    def get_all(self):
        items = self.db.query(self.entity).filter(self.entity.estado).filter(self.entity.enabled)
        return items



class PostulanteTallaManager(SuperManager):

    def __init__(self, db):
        super().__init__(PostulanteTalla, db)


    def get_all(self):
        items = self.db.query(self.entity).filter(self.entity.estado).filter(self.entity.enabled)
        return items

class PostulanteColorManager(SuperManager):
    def __init__(self, db):
        super().__init__(PostulanteColor, db)

    def get_all(self):
        items = self.db.query(self.entity).filter(self.entity.estado).filter(self.entity.enabled)
        return items