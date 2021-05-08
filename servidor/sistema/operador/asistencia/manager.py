from servidor.common.managers import SuperManager
from servidor.sistema.usuarios.bitacora.manager import BitacoraManager
from servidor.sistema.usuarios.usuario.manager import UsuarioManager
from servidor.sistema.usuarios.bitacora.model import Bitacora
from servidor.sistema.operador.asistencia.model import Asistencia,TipoAusencia

from datetime import datetime

import pytz

global fecha_zona
fecha_zona = datetime.now(pytz.timezone('America/La_Paz'))


class AsistenciaManager(SuperManager):

    def __init__(self, db):
        super().__init__(Asistencia, db)


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
        privilegios = UsuarioManager(self.db).get_privileges(idu, '/asistencia')
        datos = self.db.query(self.entity).filter(self.entity.enabled).all()
        list = []

        for item in datos:
            is_active = item.estado
            # disable = 'disabled' if 'asistencia_update' not in privilegios else ''
            disable = ''
            estado = 'Activo' if is_active else 'Inactivo'
            check = 'checked' if is_active else ''
            delete = 'asistencia_delete' in privilegios


            diccionario = item.get_dict()
            diccionario['estado'] = estado
            diccionario['check'] = check
            diccionario['disable'] = disable
            diccionario['delete'] = delete
            diccionario['fechar'] = item.fechar.strftime('%d/%m/%Y %H:%M')
            diccionario['nombre'] = item.personal.fullname
            diccionario['codigo'] = item.cliente.dia if item.fkcliente else ''
            diccionario['cliente'] = item.cliente.nombre if item.fkcliente else ''
            diccionario['ausencia'] = item.tipoausencia.nombre if item.fktipoausencia else ''

            list.append(diccionario)

        return list

    def insert(self, diccionary):

        for dict in diccionary['detalle']:
            if dict['fktipoausencia'] == "":
                dict['fktipoausencia'] = None

            if dict['fkcliente'] == "":
                dict['fkcliente'] = None

            objeto = self.entity(**dict)
            fecha = BitacoraManager(self.db).fecha_actual()

            objeto.fechar = fecha

            a = super().insert(objeto)
            b = Bitacora(fkusuario=diccionary['user'], ip=diccionary['ip'], accion="Registró asistencia.", fecha=fecha, tabla="almacen_asistencia", identificador=a.id)
            super().insert(b)

        return a

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modificó asistencia.", fecha=fecha, tabla="almacen_asistencia", identificador=a.id)
        super().insert(b)
        return a


    def update_x_stock(self, stock):
        asistenciaActual = self.db.query(self.entity).filter(self.entity.id == stock.fkasistencia).first()

        asistenciaActual.cantidad = int(asistenciaActual.cantidad) + int(stock.cantidad)
        asistenciaActual.talla = stock.talla.nombre
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(asistenciaActual)
        b = Bitacora(fkusuario=stock.user, ip=stock.ip, accion="Modificó cantidad asistencia.", fecha=fecha,
                     tabla="almacen_asistencia", identificador=a.id)
        
        super().insert(b)
        return a

    def update_detalle(self, stockDetalle):

        for det in stockDetalle:

            asistenciaDetalle = self.db.query(AsistenciaDetalle).filter(AsistenciaDetalle.id == det.fkasistenciaDetalle).first()


            if asistenciaDetalle:
                asistenciaDetalle.cantidad = int(asistenciaDetalle.cantidad) + int(det.cantidad)
                super().update(asistenciaDetalle)

        self.db.commit()


    def update_detalle_asignacion(self, asignacionDetalle):

        for det in asignacionDetalle:

            asistenciaDetalle = self.db.query(AsistenciaDetalle).filter(AsistenciaDetalle.id == det.fkasistenciaDetalle).first()


            if asistenciaDetalle:
                asistenciaDetalle.cantidad = int(asistenciaDetalle.cantidad) - int(det.cantidad)
                super().update(asistenciaDetalle)

        self.db.commit()


    def state(self, id, estado, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        mensaje = "Habilitó asistencia" if estado else "Deshabilitó asistencia"
        x.estado = estado

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion=mensaje, fecha=fecha, tabla="almacen_asistencia", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()
        return x

    def delete(self, id, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = False

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó asistencia", fecha=fecha, tabla="almacen_asistencia", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()



class TipoAusenciaManager(SuperManager):

    def __init__(self, db):
        super().__init__(TipoAusencia, db)


    def get_all(self):
        items = self.db.query(self.entity).filter(self.entity.estado).filter(self.entity.enabled)
        return items



