from servidor.common.controllers import CrudController
from servidor.sistema.almacen.subalmacen.manager import SubAlmacenManager

import json


class SubAlmacenController(CrudController):
    manager = SubAlmacenManager
    html_index = "sistema/almacen/subalmacen/views/index.html"

    routes = {
        '/subalmacen': {'GET': 'index', 'POST': 'table'},
        '/subalmacen_insert': {'POST': 'insert'},
        '/subalmacen_update': {'PUT': 'edit', 'POST': 'update'},
        '/subalmacen_state': {'POST': 'state'},
        '/subalmacen_delete': {'POST': 'delete'},
        '/subalmacen_list': {'POST': 'data_list'},
        '/subalmacen_listar': {'POST': 'listar'},
        '/subalmacen_listar_x_almacen': {'POST': 'listar_x_almacen'}

    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        us = self.get_user()

        return aux


    def listar_x_almacen(self):
        self.set_session()
        us = self.get_user()

        data = json.loads(self.get_argument("object"))
        arraT = self.manager(self.db).get_page(1, 10, None, None, True)
        arraT['objeto'] = SubAlmacenManager(self.db).listar_x_almacen(data['fkalmacen'])
        self.respond([item.get_dict() for item in arraT['objeto']])
        self.db.close()


    def listar(self):
        self.set_session()
        data = json.loads(self.get_argument("object"))
        arraT = self.manager(self.db).get_page(1, 10, None, None, True)
        arraT['objeto'] = SubAlmacenManager(self.db).listar_habilitados()
        self.respond([item.get_dict() for item in arraT['objeto']])
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
            SubAlmacenManager(self.db).insert(objeto)
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
            SubAlmacenManager(self.db).update(objeto)
            self.respond(success=True, message='Modificado correctamente.')
        except Exception as e:
            print(e)
            self.respond(response=[], success=False, message=str(e))
        self.db.close()

    def state(self):
        try:
            self.set_session()
            diccionary = json.loads(self.get_argument("object"))
            result = SubAlmacenManager(self.db).state(diccionary['id'], diccionary['estado'], self.get_user_id(), self.request.remote_ip)

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
