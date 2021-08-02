from servidor.common.managers import SuperManager
from servidor.sistema.usuarios.bitacora.manager import BitacoraManager
from servidor.sistema.usuarios.usuario.manager import UsuarioManager
from servidor.sistema.usuarios.bitacora.model import Bitacora
from servidor.sistema.recursos_humanos.motivo.model import Motivo

from datetime import datetime

import pytz

global fecha_zona
fecha_zona = datetime.now(pytz.timezone('America/La_Paz'))


class MotivoManager(SuperManager):

    def __init__(self, db):
        super().__init__(Motivo, db)

    def obtener_monto(self,idMotivo):
        items = self.db.query(self.entity).filter(self.entity.estado).filter(self.entity.enabled).filter(self.entity.id == idMotivo).first()
        return items.monto

    def listar_habilitados(self):
        return self.db.query(self.entity).filter(self.entity.estado).filter(self.entity.enabled).all()

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled).all()

    def listar_x_descuento(self):
        return self.db.query(self.entity).filter(self.entity.tipo == "Descuento").filter(self.entity.estado).filter(self.entity.enabled).all()

    def listar_x_sancion(self):
        return self.db.query(self.entity).filter(self.entity.tipo == "Sancion").filter(self.entity.estado).filter(self.entity.enabled).all()

    def list_all(self):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled))

    def get_all(self):
        items = self.db.query(self.entity).filter(self.entity.estado).filter(self.entity.enabled)
        return items

    def get_all_descuento(self):
        items = self.db.query(self.entity).filter(self.entity.estado).filter(self.entity.enabled).filter(self.entity.tipo == "Descuento")
        return items

    def get_all_sancion(self):
        items = self.db.query(self.entity).filter(self.entity.estado).filter(self.entity.enabled).filter(self.entity.tipo == "Sancion")
        return items
    

    def all_data(self, idu):
        privilegios = UsuarioManager(self.db).get_privileges(idu, '/motivo')
        datos = self.db.query(self.entity).filter(self.entity.enabled).all()
        list = []

        for item in datos:
            is_active = item.estado
            disable = 'disabled' if 'motivo_update' not in privilegios else ''
            estado = 'Activo' if is_active else 'Inactivo'
            check = 'checked' if is_active else ''
            delete = 'motivo_delete' in privilegios

            diccionario = item.get_dict()
            diccionario['estado'] = estado
            diccionario['check'] = check
            diccionario['disable'] = disable
            diccionario['delete'] = delete
            diccionario['tipo'] = item.tipo
            list.append(diccionario)

        return list
