from servidor.common.managers import SuperManager
from servidor.sistema.usuarios.bitacora.manager import BitacoraManager
from servidor.sistema.usuarios.usuario.manager import UsuarioManager
from servidor.sistema.usuarios.bitacora.model import Bitacora
from servidor.sistema.almacen.material.model import Material,MaterialDetalle,MaterialTipo,MaterialColor,MaterialTalla,MaterialAlmacenStock
from servidor.sistema.almacen.almacen.model import AlmacenSubalmacen
from servidor.sistema.almacen.asignacion.model import StockAsignacionAlmacen

from datetime import datetime

from sqlalchemy.sql import func


import pytz

global fecha_zona
fecha_zona = datetime.now(pytz.timezone('America/La_Paz'))


class MaterialManager(SuperManager):

    def __init__(self, db):
        super().__init__(Material, db)

    def listar_x_tipo(self, idtipo):

        return self.db.query(Material).filter(Material.fktipo == idtipo).order_by(
            Material.id.asc()).all()


    def listar_detalle(self, idMaterial):

        return self.db.query(MaterialDetalle).filter(MaterialDetalle.fkmaterial == idMaterial).order_by(MaterialDetalle.id.asc()).all()


    def listar_detalle_saldos(self, idMaterial,fkalmacen):

        lista_detalle = []
        for material_detalle in self.db.query(MaterialDetalle).filter(MaterialDetalle.fkmaterial == idMaterial).order_by(MaterialDetalle.id.asc()).all():
            almacen_subalmacen_nuevo = self.db.query(AlmacenSubalmacen).filter(AlmacenSubalmacen.fkalmacen == fkalmacen) \
                .filter(AlmacenSubalmacen.fksubalmacen == 1).first()

            almacen_subalmacen_usado = self.db.query(AlmacenSubalmacen).filter(AlmacenSubalmacen.fkalmacen == fkalmacen) \
                .filter(AlmacenSubalmacen.fksubalmacen == 2).first()


            almacen_material_nuevo = self.db.query(MaterialAlmacenStock).filter(MaterialAlmacenStock.fkdetallematerial == material_detalle.id) \
                .filter(MaterialAlmacenStock.fksubalmacen == almacen_subalmacen_nuevo.id).first()

            almacen_material_usado = self.db.query(MaterialAlmacenStock).filter(MaterialAlmacenStock.fkdetallematerial == material_detalle.id) \
                .filter(MaterialAlmacenStock.fksubalmacen == almacen_subalmacen_usado.id).first()


            lista_detalle.append(dict(id=material_detalle.id, material=material_detalle.material.nombre,
                                       color=material_detalle.color.nombre,talla=material_detalle.talla.nombre,nuevo=almacen_material_nuevo.cantidad,usado= almacen_material_usado.cantidad))

        return lista_detalle


    def listar_detalle_saldo_subalmacen(self, idMaterial,fksubalmacen):

        lista_detalle = []

        for material_detalle in self.db.query(MaterialDetalle).filter(MaterialDetalle.fkmaterial == idMaterial).order_by(MaterialDetalle.id.asc()).all():

            almacen_material_saldo = self.db.query(MaterialAlmacenStock).filter(MaterialAlmacenStock.fkdetallematerial == material_detalle.id) \
                .filter(MaterialAlmacenStock.fksubalmacen == fksubalmacen).first()

            lista_detalle.append(dict(id=material_detalle.id, material=material_detalle.material.nombre,
                                       color=material_detalle.color.nombre,talla=material_detalle.talla.nombre,cantidad=almacen_material_saldo.cantidad))

        return lista_detalle

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

            lista_detalle = []
            for _detalle in item.detalle:
                lista_detalle.append(dict(color=_detalle.color.nombre,talla=_detalle.talla.nombre))


            diccionario = item.get_dict()
            diccionario['estado'] = estado
            diccionario['check'] = check
            diccionario['disable'] = disable
            diccionario['delete'] = delete
            diccionario['tipo'] = item.tipo.nombre
            diccionario['nombre'] = item.nombre
            diccionario['detalle'] = lista_detalle
            diccionario['cantUsado'] = 0

            list.append(diccionario)

            # for _detalle in item.detalle:
            #
            #     diccionario = item.get_dict()
            #     diccionario['estado'] = estado
            #     diccionario['check'] = check
            #     diccionario['disable'] = disable
            #     diccionario['delete'] = delete
            #     diccionario['tipo'] = item.tipo.nombre
            #     diccionario['nombre'] = item.nombre
            #     diccionario['color'] = _detalle.color.nombre
            #     diccionario['talla'] = _detalle.talla.nombre
            #     diccionario['cantUsado'] = 0
            #
            #     list.append(diccionario)

        return list

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)

        for det in a.detalle:
            for almacen in self.db.query(AlmacenSubalmacen).filter(AlmacenSubalmacen.estado).filter(AlmacenSubalmacen.enabled).all():
                self.db.add(MaterialAlmacenStock(fkdetallematerial=det.id, fksubalmacen=almacen.id))

        self.db.commit()

        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registró material.", fecha=fecha, tabla="almacen_material", identificador=a.id)
        super().insert(b)
        return a

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        x = self.db.query(self.entity).filter(self.entity.id == a.id).first()
        for det in x.detalle:
            for almacen in self.db.query(AlmacenSubalmacen).filter(AlmacenSubalmacen.estado).filter(AlmacenSubalmacen.enabled).all():
                if self.db.query(MaterialAlmacenStock).filter(MaterialAlmacenStock.fkdetallematerial ==det.id).filter(MaterialAlmacenStock.fksubalmacen ==almacen.id).first() == None:
                    self.db.add(MaterialAlmacenStock(fkdetallematerial=det.id, fksubalmacen=almacen.id))

        self.db.commit()
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modificó material.", fecha=fecha, tabla="almacen_material", identificador=a.id)
        super().insert(b)
        return a


    def update_x_stock(self, stockdetalle,user,ip):

        for stock in stockdetalle:

            for stockdet in stock.detallestock:

                almacenSubalmacen = self.db.query(AlmacenSubalmacen)\
                    .filter(AlmacenSubalmacen.fkalmacen == stock.fkalmacen)\
                    .filter(AlmacenSubalmacen.fksubalmacen == stockdet.fksubalmacen).first()

                materialActual = self.db.query(MaterialAlmacenStock) \
                    .filter(MaterialAlmacenStock.fkdetallematerial == stock.fkmaterialDetalle) \
                    .filter(MaterialAlmacenStock.fksubalmacen == almacenSubalmacen.id).first()

                materialActual.cantidad = int(materialActual.cantidad) + int(stockdet.cantidad)

                fecha = BitacoraManager(self.db).fecha_actual()

                a = super().update(materialActual)
                b = Bitacora(fkusuario=user, ip=ip, accion="Modificó cantidad material ingreso de stock.", fecha=fecha,
                             tabla="almacen_almacen_subalmacen", identificador=materialActual.id)

                super().insert(b)

    def update_detalle_asignacion(self, asignacionDetalle,user,ip):

        for det in asignacionDetalle:

            for stockdet in det.asignacionstock:

                almacenSubalmacen = self.db.query(AlmacenSubalmacen)\
                    .filter(AlmacenSubalmacen.fkalmacen == det.fkalmacen)\
                    .filter(AlmacenSubalmacen.fksubalmacen == stockdet.fksubalmacen).first()

                materialActual = self.db.query(MaterialAlmacenStock) \
                    .filter(MaterialAlmacenStock.fkdetallematerial == det.fkmaterialDetalle) \
                    .filter(MaterialAlmacenStock.fksubalmacen == almacenSubalmacen.id).first()

                materialActual.cantidad = int(materialActual.cantidad) - int(stockdet.cantidad)

                fecha = BitacoraManager(self.db).fecha_actual()

                a = super().update(materialActual)
                b = Bitacora(fkusuario=user, ip=ip, accion="Modificó cantidad material entrega de material.", fecha=fecha,
                             tabla="almacen_almacen_subalmacen", identificador=materialActual.id)

                super().insert(b)

        self.db.commit()

    def update_traspaso(self, traspaso,user,ip):

        for det in traspaso.detalle:

            materialActualAlmacenOrigen = self.db.query(MaterialAlmacenStock) \
                .filter(MaterialAlmacenStock.fkdetallematerial == det.fkmaterialDetalle) \
                .filter(MaterialAlmacenStock.fksubalmacen == traspaso.fksubalmacenorigen).first()


            materialActualAlmacenDestino = self.db.query(MaterialAlmacenStock) \
                .filter(MaterialAlmacenStock.fkdetallematerial == det.fkmaterialDetalle) \
                .filter(MaterialAlmacenStock.fksubalmacen == traspaso.fksubalmacendestino).first()

            materialActualAlmacenOrigen.cantidad = int(materialActualAlmacenOrigen.cantidad) - int(det.cantidad)

            materialActualAlmacenDestino.cantidad = int(materialActualAlmacenDestino.cantidad) + int(det.cantidad)

            fecha = BitacoraManager(self.db).fecha_actual()

            a = super().update(materialActualAlmacenOrigen)
            d = super().update(materialActualAlmacenDestino)
            b = Bitacora(fkusuario=user, ip=ip, accion="Modificó cantidad material entrega de material.", fecha=fecha,
                         tabla="almacen_almacen_subalmacen", identificador=materialActualAlmacenOrigen.id)

            super().insert(b)

        self.db.commit()


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