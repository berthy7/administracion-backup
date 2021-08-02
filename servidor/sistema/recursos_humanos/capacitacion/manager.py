from servidor.common.managers import SuperManager
from servidor.sistema.usuarios.bitacora.manager import BitacoraManager
from servidor.sistema.usuarios.usuario.manager import UsuarioManager
from servidor.sistema.usuarios.bitacora.model import Bitacora
from servidor.sistema.recursos_humanos.capacitacion.model import Capacitacion,Tema,Titulo,Integrantes

from datetime import datetime

import pytz

global fecha_zona
fecha_zona = datetime.now(pytz.timezone('America/La_Paz'))


class CapacitacionManager(SuperManager):

    def __init__(self, db):
        super().__init__(Capacitacion, db)

    def listar_por_participacion(self,idpersonal):
        return self.db.query(Integrantes).join(Capacitacion)\
            .filter(Integrantes.fkpersonal == idpersonal)\
            .filter(Capacitacion.estado).filter(Capacitacion.enabled).all()

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
        privilegios = UsuarioManager(self.db).get_privileges(idu, '/capacitacion')
        datos = self.db.query(self.entity).filter(self.entity.enabled).all()
        list = []

        for item in datos:
            is_active = item.estado
            disable = 'disabled' if 'capacitacion_update' not in privilegios else ''
            estado = 'Activo' if is_active else 'Inactivo'
            check = 'checked' if is_active else ''
            delete = 'capacitacion_delete' in privilegios

            diccionario = item.get_dict()
            diccionario['estado'] = estado
            diccionario['check'] = check
            diccionario['disable'] = disable
            diccionario['delete'] = delete
            diccionario['fecha'] = item.fecha.strftime('%d/%m/%Y %H:%M')
            diccionario['titulo'] = item.titulo.nombre
            list.append(diccionario)

        return list

    def insert(self, diccionary):
        diccionary['fecha'] = datetime.strptime(diccionary['fecha'] +' ' + diccionary['hora'], '%d/%m/%Y %H:%M')
        objeto = CapacitacionManager(self.db).entity(**diccionary)
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registró capacitacion.", fecha=fecha, tabla="almacen_capacitacion", identificador=a.id)
        super().insert(b)
        return a

    def update(self, diccionary):
        diccionary['fecha'] = datetime.strptime(diccionary['fecha'] + ' ' + diccionary['hora'], '%d/%m/%Y %H:%M')
        objeto = CapacitacionManager(self.db).entity(**diccionary)
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modificó capacitacion.", fecha=fecha, tabla="almacen_capacitacion", identificador=a.id)
        super().insert(b)
        return a


    def state(self, id, estado, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        mensaje = "Habilitó capacitacion" if estado else "Deshabilitó capacitacion"
        x.estado = estado

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion=mensaje, fecha=fecha, tabla="almacen_capacitacion", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()
        return x

    def delete(self, id, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = False

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó capacitacion", fecha=fecha, tabla="almacen_capacitacion", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()


class TituloManager(SuperManager):

    def __init__(self, db):
        super().__init__(Titulo, db)

    def listar_habilitados(self):
        return self.db.query(self.entity).filter(self.entity.estado).filter(self.entity.enabled).all()

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled).all()

    def list_all(self):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled))

    def get_all(self):
        items = self.db.query(self.entity).filter(self.entity.estado).filter(self.entity.enabled)
        return items


class TemaManager(SuperManager):

    def __init__(self, db):
        super().__init__(Tema, db)

    def listar_habilitados(self):
        return self.db.query(self.entity).filter(self.entity.estado).filter(self.entity.enabled).all()

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled).all()

    def list_all(self):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled))

    def get_all(self):
        items = self.db.query(self.entity).filter(self.entity.estado).filter(self.entity.enabled)
        return items
