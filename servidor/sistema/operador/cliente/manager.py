from servidor.common.managers import SuperManager
from servidor.sistema.usuarios.bitacora.manager import BitacoraManager
from servidor.sistema.usuarios.usuario.manager import UsuarioManager
from servidor.sistema.usuarios.bitacora.model import Bitacora
from servidor.sistema.operador.cliente.model import Cliente

from datetime import datetime

import pytz

global fecha_zona
fecha_zona = datetime.now(pytz.timezone('America/La_Paz'))


class ClienteManager(SuperManager):

    def __init__(self, db):
        super().__init__(Cliente, db)


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
        privilegios = UsuarioManager(self.db).get_privileges(idu, '/cliente')
        datos = self.db.query(self.entity).filter(self.entity.enabled).all()
        list = []

        for item in datos:
            is_active = item.estado
            disable = 'disabled' if 'cliente_update' not in privilegios else ''
            estado = 'Activo' if is_active else 'Inactivo'
            check = 'checked' if is_active else ''
            delete = 'cliente_delete' in privilegios

            diccionario = item.get_dict()
            diccionario['estado'] = estado
            diccionario['check'] = check
            diccionario['disable'] = disable
            diccionario['delete'] = delete
            list.append(diccionario)

        return list

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registró cliente.", fecha=fecha, tabla="almacen_cliente", identificador=a.id)
        super().insert(b)
        return a

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modificó cliente.", fecha=fecha, tabla="almacen_cliente", identificador=a.id)
        super().insert(b)
        return a


    def update_x_stock(self, stock):
        clienteActual = self.db.query(self.entity).filter(self.entity.id == stock.fkcliente).first()

        clienteActual.cantidad = int(clienteActual.cantidad) + int(stock.cantidad)
        clienteActual.talla = stock.talla.nombre
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(clienteActual)
        b = Bitacora(fkusuario=stock.user, ip=stock.ip, accion="Modificó cantidad cliente.", fecha=fecha,
                     tabla="almacen_cliente", identificador=a.id)
        
        super().insert(b)
        return a

    def update_detalle(self, stockDetalle):

        for det in stockDetalle:

            clienteDetalle = self.db.query(ClienteDetalle).filter(ClienteDetalle.id == det.fkclienteDetalle).first()


            if clienteDetalle:
                clienteDetalle.cantidad = int(clienteDetalle.cantidad) + int(det.cantidad)
                super().update(clienteDetalle)

        self.db.commit()


    def update_detalle_asignacion(self, asignacionDetalle):

        for det in asignacionDetalle:

            clienteDetalle = self.db.query(ClienteDetalle).filter(ClienteDetalle.id == det.fkclienteDetalle).first()


            if clienteDetalle:
                clienteDetalle.cantidad = int(clienteDetalle.cantidad) - int(det.cantidad)
                super().update(clienteDetalle)

        self.db.commit()


    def state(self, id, estado, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        mensaje = "Habilitó cliente" if estado else "Deshabilitó cliente"
        x.estado = estado

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion=mensaje, fecha=fecha, tabla="almacen_cliente", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()
        return x

    def delete(self, id, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = False

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó cliente", fecha=fecha, tabla="almacen_cliente", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()



class ClienteTipoManager(SuperManager):

    def __init__(self, db):
        super().__init__(ClienteTipo, db)


    def get_all(self):
        items = self.db.query(self.entity).filter(self.entity.estado).filter(self.entity.enabled)
        return items



class ClienteTallaManager(SuperManager):

    def __init__(self, db):
        super().__init__(ClienteTalla, db)


    def get_all(self):
        items = self.db.query(self.entity).filter(self.entity.estado).filter(self.entity.enabled)
        return items

class ClienteColorManager(SuperManager):
    def __init__(self, db):
        super().__init__(ClienteColor, db)

    def get_all(self):
        items = self.db.query(self.entity).filter(self.entity.estado).filter(self.entity.enabled)
        return items