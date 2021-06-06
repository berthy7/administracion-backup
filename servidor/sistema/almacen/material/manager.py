from servidor.common.managers import SuperManager
from servidor.sistema.usuarios.bitacora.manager import BitacoraManager
from servidor.sistema.usuarios.usuario.manager import UsuarioManager
from servidor.sistema.usuarios.bitacora.model import Bitacora
from servidor.sistema.almacen.material.model import Material,MaterialDetalle,MaterialTipo,MaterialColor,MaterialTalla,MaterialAlmacenStock
from servidor.sistema.almacen.stock.model import StockDetalleAlmacen
from servidor.sistema.almacen.asignacion.model import StockAsignacionAlmacen

from datetime import datetime

from sqlalchemy.sql import func


import pytz

global fecha_zona
fecha_zona = datetime.now(pytz.timezone('America/La_Paz'))


class MaterialManager(SuperManager):

    def __init__(self, db):
        super().__init__(Material, db)


    def listar_detalle(self, idMaterial):

        return self.db.query(MaterialDetalle).filter(MaterialDetalle.fkmaterial == idMaterial).order_by(MaterialDetalle.id.asc()).all()

    def listar_habilitados(self):
        return self.db.query(self.entity).filter(self.entity.estado).filter(self.entity.enabled).all()

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled).all()

    def list_all(self):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled))

    def get_all(self):
        items = self.db.query(self.entity).filter(self.entity.estado).filter(self.entity.enabled).order_by(self.entity.id.asc())
        return items

    def all_data(self, idu):
        privilegios = UsuarioManager(self.db).get_privileges(idu, '/material')
        datos = self.db.query(self.entity).filter(self.entity.enabled).all()
        list = []

        for item in datos:
            is_active = item.estado
            # disable = 'disabled' if 'material_update' not in privilegios else ''
            disable = ''
            estado = 'Activo' if is_active else 'Inactivo'
            check = 'checked' if is_active else ''
            delete = 'material_delete' in privilegios

            for _detalle in item.detalle:

                diccionario = item.get_dict()
                diccionario['estado'] = estado
                diccionario['check'] = check
                diccionario['disable'] = disable
                diccionario['delete'] = delete
                diccionario['tipo'] = item.tipo.nombre
                diccionario['nombre'] = item.nombre
                diccionario['color'] = _detalle.color.nombre
                diccionario['talla'] = _detalle.talla.nombre

                list.append(diccionario)

        return list

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)

        # for det in a.detalle:
        #     for almacen in self.db.query(MaterialAlmacen).filter(MaterialAlmacen.estado).filter(MaterialAlmacen.enabled).all():
        #         self.db.add(MaterialAlmacenStock(fkdetallematerial=det.id, fkalmacen=almacen.id, cantidad=0))
        #
        # self.db.commit()

        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registró material.", fecha=fecha, tabla="almacen_material", identificador=a.id)
        super().insert(b)
        return a

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modificó material.", fecha=fecha, tabla="almacen_material", identificador=a.id)
        super().insert(b)
        return a


    def update_x_stock(self, stock):
        materialActual = self.db.query(self.entity).filter(self.entity.id == stock.fkmaterial).first()

        materialActual.cantidad = int(materialActual.cantidad) + int(stock.cantidad)
        materialActual.talla = stock.talla.nombre
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(materialActual)
        b = Bitacora(fkusuario=stock.user, ip=stock.ip, accion="Modificó cantidad material.", fecha=fecha,
                     tabla="almacen_material", identificador=a.id)
        
        super().insert(b)
        return a

    # def update_detalle(self, stockDetalle):
    #
    #     for det in stockDetalle:
    #
    #
    #
    #         almacen = self.db.query(MaterialAlmacen).all()
    #
    #         for alma in almacen:
    #
    #             stockDetalleAlmacen = self.db.query(StockDetalleAlmacen) \
    #                 .filter(StockDetalleAlmacen.fkstockdetalle == det.id)\
    #                 .filter(StockDetalleAlmacen.fkalmacen == alma.id).first()
    #
    #             if stockDetalleAlmacen:
    #                 materialAlmacen = self.db.query(MaterialAlmacenStock) \
    #                     .filter(MaterialAlmacenStock.fkdetallematerial == det.fkmaterialDetalle) \
    #                     .filter(MaterialAlmacenStock.fkalmacen == alma.id).first()
    #
    #                 materialAlmacen.cantidad = int(materialAlmacen.cantidad) + int(stockDetalleAlmacen.cantidad)
    #
    #                 self.db.merge(materialAlmacen)
    #                 self.db.commit()
    #
    #         # if materialDetalle:
    #         #     materialDetalle.cantidad = int(materialDetalle.cantidad) + int(det.cantidad)
    #         #     super().update(materialDetalle)
    #
    #     self.db.commit()
    #
    #
    # def update_detalle_asignacion(self, asignacionDetalle):
    #
    #     for det in asignacionDetalle:
    #
    #         almacen = self.db.query(MaterialAlmacen).all()
    #         for alma in almacen:
    #
    #             stockAsignacionAlmacen = self.db.query(StockAsignacionAlmacen) \
    #                 .filter(StockAsignacionAlmacen.fkasignaciondetalle == det.id)\
    #                 .filter(StockAsignacionAlmacen.fkalmacen == alma.id).first()
    #
    #             if stockAsignacionAlmacen:
    #                 materialAlmacen = self.db.query(MaterialAlmacenStock) \
    #                     .filter(MaterialAlmacenStock.fkdetallematerial == det.fkmaterialDetalle) \
    #                     .filter(MaterialAlmacenStock.fkalmacen == alma.id).first()
    #
    #                 materialAlmacen.cantidad = int(materialAlmacen.cantidad) - int(stockAsignacionAlmacen.cantidad)
    #                 self.db.merge(materialAlmacen)
    #                 self.db.commit()
    #
    #     self.db.commit()


    def state(self, id, estado, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        mensaje = "Habilitó material" if estado else "Deshabilitó material"
        x.estado = estado

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion=mensaje, fecha=fecha, tabla="almacen_material", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()
        return x

    def delete(self, id, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = False

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó material", fecha=fecha, tabla="almacen_material", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()



class MaterialTipoManager(SuperManager):

    def __init__(self, db):
        super().__init__(MaterialTipo, db)


    def get_all(self):
        items = self.db.query(self.entity).filter(self.entity.estado).filter(self.entity.enabled)
        return items



class MaterialTallaManager(SuperManager):

    def __init__(self, db):
        super().__init__(MaterialTalla, db)


    def get_all(self):
        items = self.db.query(self.entity).filter(self.entity.estado).filter(self.entity.enabled)
        return items

class MaterialColorManager(SuperManager):
    def __init__(self, db):
        super().__init__(MaterialColor, db)

    def get_all(self):
        items = self.db.query(self.entity).filter(self.entity.estado).filter(self.entity.enabled)
        return items