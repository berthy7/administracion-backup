from servidor.common.controllers import CrudController
from servidor.sistema.recursos_humanos.capacitacion.manager import CapacitacionManager
from servidor.sistema.recursos_humanos.personal.manager import PersonalManager



import json


class CapacitacionController(CrudController):
    manager = CapacitacionManager
    html_index = "sistema/recursos_humanos/capacitacion/views/index.html"

    routes = {
        '/capacitacion': {'GET': 'index', 'POST': 'table'},
        '/capacitacion_insert': {'POST': 'insert'},
        '/capacitacion_update': {'PUT': 'edit', 'POST': 'update'},
        '/capacitacion_state': {'POST': 'state'},
        '/capacitacion_delete': {'POST': 'delete'},
        '/capacitacion_list': {'POST': 'data_list'},
        '/capacitacion_listar_detalle': {'POST': 'listar_detalle'}
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        us = self.get_user()
        aux['personales'] = PersonalManager(self.db).listar_habilitados()

        return aux

    def listar_detalle(self):

        self.set_session()

        data = json.loads(self.get_argument("object"))
        arraT = self.manager(self.db).get_page(1, 10, None, None, True)
        arraT['objeto'] = CapacitacionManager(self.db).listar_detalle(data['idCapacitacion'])
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

            CapacitacionManager(self.db).insert(diccionary)
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
            CapacitacionManager(self.db).update(objeto)
            self.respond(success=True, message='Modificado correctamente.')
        except Exception as e:
            print(e)
            self.respond(response=[], success=False, message=str(e))
        self.db.close()

    def state(self):
        try:
            self.set_session()
            diccionary = json.loads(self.get_argument("object"))
            result = CapacitacionManager(self.db).state(diccionary['id'], diccionary['estado'], self.get_user_id(), self.request.remote_ip)

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
