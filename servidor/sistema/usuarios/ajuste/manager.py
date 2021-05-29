from servidor.common.managers import SuperManager
from servidor.sistema.usuarios.bitacora.manager import BitacoraManager
from servidor.sistema.usuarios.usuario.manager import UsuarioManager
from servidor.sistema.usuarios.bitacora.model import Bitacora
from servidor.sistema.usuarios.ajuste.model import Ajuste

from datetime import datetime

import pytz

global fecha_zona
fecha_zona = datetime.now(pytz.timezone('America/La_Paz'))


class AjusteManager(SuperManager):

    def __init__(self, db):
        super().__init__(Ajuste, db)

    def obtener(self):

        x = self.db.query(self.entity).filter(self.entity.enabled == True).first()

        return dict(id=x.id,claveSecreta=x.claveSecreta)


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
        privilegios = UsuarioManager(self.db).get_privileges(idu, '/grado')
        datos = self.db.query(self.entity).filter(self.entity.enabled).all()
        list = []

        for item in datos:

            disable = 'disabled' if 'grado_update' not in privilegios else ''

            delete = 'grado_delete' in privilegios

            diccionario = item.get_dict()
            diccionario['disable'] = disable
            diccionario['delete'] = delete
            list.append(diccionario)

        return list

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registró grado.", fecha=fecha, tabla="parametrizacion_grado", identificador=a.id)
        super().insert(b)
        return a

    def update(self, diccionario):
        objeto = self.db.query(self.entity).filter(self.entity.enabled == True).first()

        fecha = BitacoraManager(self.db).fecha_actual()
        objeto.claveSecreta = diccionario['clavesecreta']

        a = super().update(objeto)
        b = Bitacora(fkusuario=diccionario['user'], ip=diccionario['ip'], accion="Modificó Clave Secreta.", fecha=fecha, tabla="usuarios_ajuste", identificador=a.id)
        super().insert(b)
        return a

    def state(self, id, estado, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        mensaje = "Habilitó grado" if estado else "Deshabilitó grado"
        x.estado = estado

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion=mensaje, fecha=fecha, tabla="parametrizacion_grado", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()
        return x

    def delete(self, id, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = False

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó grado", fecha=fecha, tabla="parametrizacion_grado", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()
