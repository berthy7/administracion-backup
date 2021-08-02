from servidor.common.controllers import CrudController
from servidor.sistema.operador.sancion.manager import SancionManager
from servidor.sistema.recursos_humanos.personal.manager import PersonalManager
from servidor.sistema.recursos_humanos.motivo.manager import MotivoManager


import os.path
import uuid
import json


class SancionController(CrudController):
    manager = SancionManager
    html_index = "sistema/operador/sancion/views/index.html"

    routes = {
        '/sancion': {'GET': 'index', 'POST': 'table'},
        '/sancion_insert': {'POST': 'insert'},
        '/sancion_update': {'PUT': 'edit', 'POST': 'update'},
        '/sancion_state': {'POST': 'state'},
        '/sancion_delete': {'POST': 'delete'},
        '/sancion_list': {'POST': 'data_list'},
        '/sancion_importar': {'POST': 'importar'},
        '/sancion_reporte_excel': {'POST': 'reporte_excel'}
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        aux['personales'] = PersonalManager(self.db).get_all()
        aux['motivos'] = MotivoManager(self.db).get_all_sancion()
        us = self.get_user()

        return aux

    def reporte_excel(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))

        cname = self.manager(self.db).sancion_excel(diccionary)
        self.respond({'nombre': cname, 'url': 'resources/downloads/' + cname}, True)
        self.db.close()


    def importar(self):
        self.set_session()
        fileinfo = self.request.files['archivo'][0]
        fname = fileinfo['filename']
        extn = os.path.splitext(fname)[1]
        cname = str(uuid.uuid4()) + extn
        fh = open("servidor/common/resources/uploads/" + cname, 'wb')
        fh.write(fileinfo['body'])
        fh.close()
        if extn in ['.xlsx', '.xls']:
            mee = self.manager(self.db).importar_excel(cname,self.get_user_id(),self.request.remote_ip)
            self.respond(message=mee['message'], success=mee['success'])
        else:
            self.respond(message='Formato de Archivo no aceptado¡¡', success=False)
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
            dicc_foto = dict()
            list_doc = list()
            diccionary = json.loads(self.get_argument("object"))
            diccionary['user'] = self.get_user_id()
            diccionary['ip'] = self.request.remote_ip

            list_doc.append(dicc_foto)
            diccionary['documentos'] = list_doc

            objeto = self.manager(self.db).entity(**diccionary)

            SancionManager(self.db).insert(objeto)
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
            SancionManager(self.db).update(objeto)
            self.respond(success=True, message='Modificado correctamente.')
        except Exception as e:
            print(e)
            self.respond(response=[], success=False, message=str(e))
        self.db.close()

    def state(self):
        try:
            self.set_session()
            diccionary = json.loads(self.get_argument("object"))
            result = SancionManager(self.db).state(diccionary['id'], diccionary['estado'], self.get_user_id(), self.request.remote_ip)

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
