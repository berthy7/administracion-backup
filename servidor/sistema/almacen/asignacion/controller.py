from servidor.common.controllers import CrudController
from servidor.sistema.almacen.asignacion.manager import AsignacionManager
from servidor.sistema.recursos_humanos.personal.manager import PersonalManager
from servidor.sistema.almacen.material.manager import MaterialManager,MaterialColorManager,MaterialTallaManager

import os.path
import uuid
import json
from xhtml2pdf import pisa


class AsignacionController(CrudController):
    manager = AsignacionManager
    html_index = "sistema/almacen/asignacion/views/index.html"

    routes = {
        '/asignacion': {'GET': 'index', 'POST': 'table'},
        '/asignacion_insert': {'POST': 'insert'},
        '/asignacion_update': {'PUT': 'edit', 'POST': 'update'},
        '/asignacion_devolucion': {'PUT': 'edit_Devolucion', 'POST': 'update_Devolucion'},
        '/asignacion_state': {'POST': 'state'},
        '/asignacion_delete': {'POST': 'delete'},
        '/asignacion_list': {'POST': 'data_list'},
    }

    def get_extra_data(self):
        aux = super().get_extra_data()

        aux['personales'] = PersonalManager(self.db).get_all()

        aux['materiales_detalle'] = MaterialManager(self.db).get_all()

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
            if "foto" in self.request.files:
                fileinfo = self.request.files["foto"][0]
                fname = fileinfo.filename
                extn = os.path.splitext(fname)[1]
                cname = str(uuid.uuid4()) + extn
                f = open("servidor/common/resources/images/foto_personal/" + cname, 'wb')
                f.write(fileinfo.body)
                f.close()
                diccionary['foto'] = "/resources/images/foto_personal/" + cname
                PersonalManager(self.db).actualizar_foto(diccionary['fkpersonal'],diccionary['foto'],diccionary['user'],diccionary['ip'])

            objeto = self.manager(self.db).entity(**diccionary)
            AsignacionManager(self.db).insert(objeto)
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
            if "foto" in self.request.files:
                fileinfo = self.request.files["foto"][0]
                fname = fileinfo.filename
                extn = os.path.splitext(fname)[1]
                cname = str(uuid.uuid4()) + extn
                f = open("servidor/common/resources/images/foto_personal/" + cname, 'wb')
                f.write(fileinfo.body)
                f.close()
                diccionary['foto'] = "/resources/images/foto_personal/" + cname
                PersonalManager(self.db).actualizar_foto(diccionary['fkpersonal'],diccionary['foto'],diccionary['user'],diccionary['ip'])

            objeto = self.manager(self.db).entity(**diccionary)
            AsignacionManager(self.db).update(objeto)
            self.respond(success=True, message='Modificado correctamente.')
        except Exception as e:
            print(e)
            self.respond(response=[], success=False, message=str(e))
        self.db.close()

    def state(self):
        try:
            self.set_session()
            diccionary = json.loads(self.get_argument("object"))
            result = AsignacionManager(self.db).state(diccionary['id'], diccionary['estado'], self.get_user_id(), self.request.remote_ip)

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


    def edit_Devolucion(self):
        self.set_session()
        # self.verif_privileges()
        ins_manager = self.manager(self.db)
        diccionary = json.loads(self.get_argument("object"))
        indicted_object = ins_manager.obtener_para_devolucion(diccionary['id'])

        if len(ins_manager.errors) == 0:
            self.respond(indicted_object, message='Operación exitosa!')
        else:
            self.respond([item.__dict__ for item in ins_manager.errors], False, 'Ocurrió un error al insertar')
        self.db.close()