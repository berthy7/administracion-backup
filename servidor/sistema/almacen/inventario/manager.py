from servidor.common.managers import SuperManager
from servidor.sistema.usuarios.bitacora.manager import BitacoraManager
from servidor.sistema.usuarios.usuario.manager import UsuarioManager
from servidor.sistema.usuarios.bitacora.model import Bitacora
from servidor.sistema.almacen.material.model import Material,MaterialAlmacenStock
from servidor.sistema.almacen.almacen.model import AlmacenSubalmacen

from datetime import datetime

import pytz

global fecha_zona
fecha_zona = datetime.now(pytz.timezone('America/La_Paz'))


class InventarioManager(SuperManager):

    def __init__(self, db):
        super().__init__(Material, db)

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
        privilegios = UsuarioManager(self.db).get_privileges(idu, '/inventario')
        datos = self.db.query(self.entity).filter(self.entity.enabled).all()
        list = []

        lista_titulos = []

        datos_almacen = self.db.query(AlmacenSubalmacen).filter(AlmacenSubalmacen.enabled).all()

        sw_titulos = 0

        for item in datos:

            for _detalle in item.detalle:

                diccionario = item.get_dict()
                diccionario['detalle_id'] = _detalle.id
                diccionario['tipo'] = item.tipo.nombre
                diccionario['nombre'] = item.nombre
                diccionario['color'] = _detalle.color.nombre
                diccionario['talla'] = _detalle.talla.nombre

                for _almacen in datos_almacen:
                    saldo_almacen = self.db.query(MaterialAlmacenStock).filter(MaterialAlmacenStock.fkdetallematerial == _detalle.id).filter(MaterialAlmacenStock.fksubalmacen == _almacen.id).first()
                    diccionario[_almacen.almacen.nombre + " "+_almacen.subalmacen.nombre] = str(saldo_almacen.cantidad)

                    if sw_titulos ==0 :
                        lista_titulos.append(_almacen.almacen.nombre + " "+_almacen.subalmacen.nombre)

                diccionario['titulos'] = lista_titulos
                list.append(diccionario)
                sw_titulos = 1



        return list

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registró inventario.", fecha=fecha, tabla="almacen_inventario", identificador=a.id)
        super().insert(b)
        return a

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modificó inventario.", fecha=fecha, tabla="almacen_inventario", identificador=a.id)
        super().insert(b)
        return a

    def state(self, id, estado, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        mensaje = "Habilitó inventario" if estado else "Deshabilitó inventario"
        x.estado = estado

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion=mensaje, fecha=fecha, tabla="almacen_inventario", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()
        return x

    def delete(self, id, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = False

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó inventario", fecha=fecha, tabla="almacen_inventario", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()
