from servidor.common.controllers import CrudController
from servidor.sistema.almacen.material.manager import MaterialManager,MaterialTipoManager,MaterialColorManager,MaterialTallaManager


import json


class MaterialController(CrudController):
    manager = MaterialManager
    html_index = "sistema/almacen/material/views/index.html"

    routes = {
        '/material': {'GET': 'index', 'POST': 'table'},
        '/material_insert': {'POST': 'insert'},
        '/material_update': {'PUT': 'edit', 'POST': 'update'},
        '/material_state': {'POST': 'state'},
        '/material_delete': {'POST': 'delete'},
        '/material_list': {'POST': 'data_list'},
        '/material_listar_detalle': {'POST': 'listar_detalle'},
        '/material_listar_detalle_saldos': {'POST': 'listar_detalle_saldos'},
        '/material_listar_detalle_saldo_subalmacen': {'POST': 'listar_detalle_saldo_subalmacen'},
        '/material_listar_x_tipo': {'POST': 'listar_x_tipo'}
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        us = self.get_user()
        aux['tipos'] = MaterialTipoManager(self.db).get_all()
        aux['materiales'] = MaterialManager(self.db).get_all()
        aux['tallas'] = MaterialTallaManager(self.db).get_all()
        aux['colores'] = MaterialColorManager(self.db).get_all()

        return aux


    def listar_x_tipo(self):
        self.set_session()
        us = self.get_user()

        data = json.loads(self.get_argument("object"))
        arraT = self.manager(self.db).get_page(1, 10, None, None, True)
        arraT['objeto'] = MaterialManager(self.db).listar_x_tipo(data['fktipo'])
        self.respond([item.get_dict() for item in arraT['objeto']])
        self.db.close()

    def listar_detalle(self):

        self.set_session()

        data = json.loads(self.get_argument("object"))
        arraT = self.manager(self.db).get_page(1, 10, None, None, True)
        arraT['objeto'] = MaterialManager(self.db).listar_detalle(data['idMaterial'])
        self.respond([item.get_dict() for item in arraT['objeto']])
        self.db.close()


    def listar_detalle_saldos(self):

        self.set_session()

        data = json.loads(self.get_argument("object"))
        arraT = self.manager(self.db).get_page(1, 10, None, None, True)
        arraT['objeto'] = MaterialManager(self.db).listar_detalle_saldos(data['idMaterial'],data['fkalmacen'])
        self.respond(arraT['objeto'])
        self.db.close()


    def listar_detalle_saldo_subalmacen(self):

        self.set_session()

        data = json.loads(self.get_argument("object"))
        arraT = self.manager(self.db).get_page(1, 10, None, None, True)
        arraT['objeto'] = MaterialManager(self.db).listar_detalle_saldo_subalmacen(data['idMaterial'],data['fksubalmacen'])
        self.respond(arraT['objeto'])
        self.db.close()

    def data_list(self):
        try:
            self.set_session()
            user = self.get_user()
            ins_manager = self.manager(self.db)
            indicted_object = ins_manager.all_data(user.id)

            if len(ins_manager.errors) == 0:
                self.respond_ajax(indicted_object, message='Operación exitosa!')
            else:
                self.respond([item.__dict__ for item in ins_manager.errors], False, 'Ocurrió un error al consultar')
        except Exception as e:
            print(e)
            self.respond(response=[], success=False, message=str(e))
        self.db.close()

    def insert(self):
        try:
            self.set_session()
            diccionary = json.loads(self.get_argument("object"))
            diccionary['user'] = self.get_user_id()
            diccionary['ip'] = self.request.remote_ip
            objeto = self.manager(self.db).entity(**diccionary)
            MaterialManager(self.db).insert(objeto)
            self.respond(success=True, message='Registrado correctamente.')
        except Exception as e:
            print(e)
            self.respond(response=[], success=False, message=str(e))
        self.db.close()

    def update(self):
        try:
            self.set_session()
            diccionary = json.loads(self.get_argument("object"))
            diccionary['user'] = self.get_user_id()
            diccionary['ip'] = self.request.remote_ip
            objeto = self.manager(self.db).entity(**diccionary)
            MaterialManager(self.db).update(objeto)
            self.respond(success=True, message='Modificado correctamente.')
        except Exception as e:
            print(e)
            self.respond(response=[], success=False, message=str(e))
        self.db.close()

    def state(self):
        try:
            self.set_session()
            diccionary = json.loads(self.get_argument("object"))
            result = MaterialManager(self.db).state(diccionary['id'], diccionary['estado'], self.get_user_id(), self.request.remote_ip)

            if result:
                msg = 'Habilitado correctamente.' if result.estado else 'Deshabilitado correctamente.'
                self.respond(success=True, message=msg)
            else:
                self.respond(success=False, message='ERROR 403')
        except Exception as e:
            print(e)
            self.respond(response=[], success=False, message=str(e))
        self.db.close()

    def delete(self):
        try:
            self.set_session()
            diccionary = json.loads(self.get_argument("object"))
            self.manager(self.db).delete(diccionary['id'], self.get_user_id(), self.request.remote_ip)
            self.respond(success=True, message='Eliminado correctamente.')
        except Exception as e:
            print(e)
            self.respond(response=[], success=False, message=str(e))
