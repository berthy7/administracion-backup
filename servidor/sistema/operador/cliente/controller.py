from servidor.common.controllers import CrudController
from servidor.sistema.operador.cliente.manager import ClienteManager


import json


class ClienteController(CrudController):
    manager = ClienteManager
    html_index = "sistema/operador/cliente/views/index.html"

    routes = {
        '/cliente': {'GET': 'index', 'POST': 'table'},
        '/cliente_insert': {'POST': 'insert'},
        '/cliente_update': {'PUT': 'edit', 'POST': 'update'},
        '/cliente_state': {'POST': 'state'},
        '/cliente_delete': {'POST': 'delete'},
        '/cliente_list': {'POST': 'data_list'}
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        us = self.get_user()

        return aux



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
            ClienteManager(self.db).insert(objeto)
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
            ClienteManager(self.db).update(objeto)
            self.respond(success=True, message='Modificado correctamente.')
        except Exception as e:
            print(e)
            self.respond(response=[], success=False, message=str(e))
        self.db.close()

    def state(self):
        try:
            self.set_session()
            diccionary = json.loads(self.get_argument("object"))
            result = ClienteManager(self.db).state(diccionary['id'], diccionary['estado'], self.get_user_id(), self.request.remote_ip)

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
