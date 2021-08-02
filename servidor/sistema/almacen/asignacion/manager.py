from servidor.common.managers import SuperManager
from servidor.sistema.usuarios.bitacora.manager import BitacoraManager
from servidor.sistema.usuarios.usuario.manager import UsuarioManager
from servidor.sistema.usuarios.bitacora.model import Bitacora
from servidor.sistema.almacen.asignacion.model import Asignacion
from servidor.sistema.almacen.material.manager import MaterialManager

from datetime import datetime

import pytz

global fecha_zona
fecha_zona = datetime.now(pytz.timezone('America/La_Paz'))


class AsignacionManager(SuperManager):

    def __init__(self, db):
        super().__init__(Asignacion, db)

    def obtener_para_devolucion(self,idAsignacion):

        asignacion = self.db.query(self.entity).filter(self.entity.id == idAsignacion).first()

        lista_detalle = list()
        for detalle in asignacion.detalle:

            for asignacionstock in detalle.asignacionstock:

                print(asignacionstock.asignaciondetalle.materialDetalle.material.nombre)
                cant_backup = 0
                cant_usado = 0

                # for asignacionAlmacen in asignacionstock.almacen:
                #     if asignacionAlmacen.fkalmacen == 1:
                #         cant_backup = asignacion.cantidad
                #     if asignacionAlmacen.fkalmacen == 2:
                #         cant_usado = asignacion.cantidad


                lista_detalle.append(dict(id=asignacionstock.id,material=asignacionstock.asignaciondetalle.materialDetalle.material.nombre,
                                          color=asignacionstock.asignaciondetalle.materialDetalle.color.nombre,
                                          talla=asignacionstock.asignaciondetalle.materialDetalle.talla.nombre,
                                          backup =cant_backup,
                                          usado= cant_usado))



        asignacion_dict = dict(id=asignacion.id,
                               descripcion=asignacion.descripcion,
                               fkpersonal=asignacion.fkpersonal,
                               fotoPersonal=asignacion.personal.foto,
                               detalle=lista_detalle)

        return asignacion_dict

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
        privilegios = UsuarioManager(self.db).get_privileges(idu, '/asignacion')
        datos = self.db.query(self.entity).filter(self.entity.enabled).all()
        list = []

        for item in datos:
            is_active = item.estado
            # disable = 'disabled' if 'asignacion_update' not in privilegios else ''
            disable = ''
            estado = 'Activo' if is_active else 'Inactivo'
            check = 'checked' if is_active else ''
            delete = 'asignacion_delete' in privilegios

            diccionario = item.get_dict()
            diccionario['estado'] = estado
            diccionario['check'] = check
            diccionario['disable'] = disable
            diccionario['delete'] = delete
            diccionario['fechar'] = item.fechar.strftime('%d/%m/%Y %H:%M')
            diccionario['fullname'] = item.personal.fullname
            list.append(diccionario)

        return list

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()
        objeto.fechar = fecha
        a = super().insert(objeto)

        MaterialManager(self.db).update_detalle_asignacion(a.detalle,objeto.user,objeto.ip)

        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registró asignacion.", fecha=fecha, tabla="parametrizacion_asignacion", identificador=a.id)
        super().insert(b)
        return a

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modificó asignacion.", fecha=fecha, tabla="parametrizacion_asignacion", identificador=a.id)
        super().insert(b)
        return a

    def state(self, id, estado, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        mensaje = "Habilitó asignacion" if estado else "Deshabilitó asignacion"
        x.estado = estado

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion=mensaje, fecha=fecha, tabla="parametrizacion_asignacion", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()
        return x

    def delete(self, id, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = False

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó asignacion", fecha=fecha, tabla="parametrizacion_asignacion", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()
