from servidor.common.controllers import CrudController
from servidor.sistema.recursos_humanos.personal.manager import PersonalManager
from servidor.sistema.recursos_humanos.cargo.manager import CargoManager
from servidor.sistema.parametrizacion.categoria.manager import *
from servidor.sistema.parametrizacion.nacionalidad.manager import *
from servidor.sistema.parametrizacion.expedido.manager import *
from servidor.sistema.parametrizacion.civil.manager import *
from servidor.sistema.parametrizacion.parentesco.manager import *
from servidor.sistema.parametrizacion.retiro.manager import *
from servidor.sistema.parametrizacion.grado.manager import *
from servidor.sistema.parametrizacion.regimiento.manager import *

import os.path
import uuid
import json
from xhtml2pdf import pisa

class Report:
    def html_to_pdf(self, sourceHtml, nombre):
        outputFilename = 'servidor/common/resources/downloads/' + nombre

        resultFile = open(outputFilename, "w+b")
        pisaStatus = pisa.CreatePDF(
            sourceHtml,
            dest=resultFile)
        resultFile.close()

        return pisaStatus.err

global report
report = Report()

class PersonalController(CrudController):
    manager = PersonalManager
    html_index = "sistema/recursos_humanos/personal/views/index.html"

    routes = {
        '/personal': {'GET': 'index', 'POST': 'table'},
        '/personal_insert': {'POST': 'insert'},
        '/personal_update': {'PUT': 'edit', 'POST': 'update'},
        '/personal_state': {'POST': 'state'},
        '/personal_delete': {'POST': 'delete'},
        '/personal_list': {'POST': 'data_list'},
        '/personal_report': {'POST': 'report'},
        '/personal_edad': {'POST': 'obtener_edad'},
        '/personal_buscar': {'PUT': 'buscar'},
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        us = self.get_user()
        aux['nacionalidades'] = NacionalidadManager(self.db).listar_habilitados()
        aux['expedidos'] = ExpedidoManager(self.db).listar_habilitados()
        aux['categorias'] = CategoriaManager(self.db).listar_habilitados()
        aux['estados_civiles'] = CivilManager(self.db).listar_habilitados()
        aux['parentescos'] = ParentescoManager(self.db).listar_habilitados()
        aux['retiros'] = RetiroManager(self.db).listar_habilitados()
        aux['grados'] = GradoManager(self.db).listar_habilitados()
        aux['regimientos'] = RegimientoManager(self.db).get_all()
        aux['cargos'] = CargoManager(self.db).get_all()
        aux['tipocontratos'] = PersonalManager(self.db).listar_tipocontrato_habilitados()

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
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        dicc_foto = dict()
        list_doc = list()
        # if "foto" in self.request.files:
        #     fileinfo = self.request.files["foto"][0]
        #     fname = fileinfo.filename
        #     extn = os.path.splitext(fname)[1]
        #     cname = str(uuid.uuid4()) + extn
        #     f = open("servidor/common/resources/images/foto_personal/" + cname, 'wb')
        #     f.write(fileinfo.body)
        #     f.close()
        #     diccionary['foto'] = "/resources/images/foto_personal/" + cname

        if "ci" in self.request.files:
            fileinfo = self.request.files["ci"][0]
            fname = fileinfo.filename
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            f = open("servidor/common/resources/images/foto_documentos/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()
            dicc_foto['ci'] = "/resources/images/foto_documentos/" + cname

        if "flcn" in self.request.files:
            fileinfo = self.request.files["flcn"][0]
            fname = fileinfo.filename
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            f = open("servidor/common/resources/images/foto_documentos/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()
            dicc_foto['flcn'] = "/resources/images/foto_documentos/" + cname

        if "libretamilitar" in self.request.files:
            fileinfo = self.request.files["libretamilitar"][0]
            fname = fileinfo.filename
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            f = open("servidor/common/resources/images/foto_documentos/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()
            dicc_foto['libretamilitar'] = "/resources/images/foto_documentos/" + cname

        if "flcc" in self.request.files:
            fileinfo = self.request.files["flcc"][0]
            fname = fileinfo.filename
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            f = open("servidor/common/resources/images/foto_documentos/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()
            dicc_foto['flcc'] = "/resources/images/foto_documentos/" + cname

        if "titulobachiller" in self.request.files:
            fileinfo = self.request.files["titulobachiller"][0]
            fname = fileinfo.filename
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            f = open("servidor/common/resources/images/foto_documentos/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()
            dicc_foto['titulobachiller'] = "/resources/images/foto_documentos/" + cname

        if "luzagua" in self.request.files:
            fileinfo = self.request.files["luzagua"][0]
            fname = fileinfo.filename
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            f = open("servidor/common/resources/images/foto_documentos/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()
            dicc_foto['luzagua'] = "/resources/images/foto_documentos/" + cname

        if "titulotecnico" in self.request.files:
            fileinfo = self.request.files["titulotecnico"][0]
            fname = fileinfo.filename
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            f = open("servidor/common/resources/images/foto_documentos/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()
            dicc_foto['titulotecnico'] = "/resources/images/foto_documentos/" + cname

        if "certificadonacimiento" in self.request.files:
            fileinfo = self.request.files["certificadonacimiento"][0]
            fname = fileinfo.filename
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            f = open("servidor/common/resources/images/foto_documentos/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()
            dicc_foto['certificadonacimiento'] = "/resources/images/foto_documentos/" + cname

        if "titulolicenciatura" in self.request.files:
            fileinfo = self.request.files["titulolicenciatura"][0]
            fname = fileinfo.filename
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            f = open("servidor/common/resources/images/foto_documentos/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()
            dicc_foto['titulolicenciatura'] = "/resources/images/foto_documentos/" + cname

        if "flcv" in self.request.files:
            fileinfo = self.request.files["flcv"][0]
            fname = fileinfo.filename
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            f = open("servidor/common/resources/images/foto_documentos/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()
            dicc_foto['flcv'] = "/resources/images/foto_documentos/" + cname

        if "otros" in self.request.files:
            fileinfo = self.request.files["otros"][0]
            fname = fileinfo.filename
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            f = open("servidor/common/resources/images/foto_documentos/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()
            dicc_foto['otros'] = "/resources/images/foto_documentos/" + cname

        list_doc.append(dicc_foto)

        diccionary['documentos'] = list_doc


        PersonalManager(self.db).insert(diccionary)
        self.respond(success=True, message='Registrado correctamente.')

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        dicc_foto = dict()
        list_doc = list()
        # if "foto" in self.request.files:
        #     fileinfo = self.request.files["foto"][0]
        #     fname = fileinfo.filename
        #     extn = os.path.splitext(fname)[1]
        #     cname = str(uuid.uuid4()) + extn
        #     f = open("servidor/common/resources/images/foto_personal/" + cname, 'wb')
        #     f.write(fileinfo.body)
        #     f.close()
        #     diccionary['foto'] = "/resources/images/foto_personal/" + cname

        if "ci" in self.request.files:
            fileinfo = self.request.files["ci"][0]
            fname = fileinfo.filename
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            f = open("servidor/common/resources/images/foto_documentos/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()
            dicc_foto['ci'] = "/resources/images/foto_documentos/" + cname

        if "flcn" in self.request.files:
            fileinfo = self.request.files["flcn"][0]
            fname = fileinfo.filename
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            f = open("servidor/common/resources/images/foto_documentos/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()
            dicc_foto['flcn'] = "/resources/images/foto_documentos/" + cname

        if "libretamilitar" in self.request.files:
            fileinfo = self.request.files["libretamilitar"][0]
            fname = fileinfo.filename
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            f = open("servidor/common/resources/images/foto_documentos/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()
            dicc_foto['libretamilitar'] = "/resources/images/foto_documentos/" + cname

        if "flcc" in self.request.files:
            fileinfo = self.request.files["flcc"][0]
            fname = fileinfo.filename
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            f = open("servidor/common/resources/images/foto_documentos/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()
            dicc_foto['flcc'] = "/resources/images/foto_documentos/" + cname

        if "titulobachiller" in self.request.files:
            fileinfo = self.request.files["titulobachiller"][0]
            fname = fileinfo.filename
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            f = open("servidor/common/resources/images/foto_documentos/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()
            dicc_foto['titulobachiller'] = "/resources/images/foto_documentos/" + cname

        if "luzagua" in self.request.files:
            fileinfo = self.request.files["luzagua"][0]
            fname = fileinfo.filename
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            f = open("servidor/common/resources/images/foto_documentos/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()
            dicc_foto['luzagua'] = "/resources/images/foto_documentos/" + cname

        if "titulotecnico" in self.request.files:
            fileinfo = self.request.files["titulotecnico"][0]
            fname = fileinfo.filename
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            f = open("servidor/common/resources/images/foto_documentos/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()
            dicc_foto['titulotecnico'] = "/resources/images/foto_documentos/" + cname

        if "certificadonacimiento" in self.request.files:
            fileinfo = self.request.files["certificadonacimiento"][0]
            fname = fileinfo.filename
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            f = open("servidor/common/resources/images/foto_documentos/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()
            dicc_foto['certificadonacimiento'] = "/resources/images/foto_documentos/" + cname

        if "titulolicenciatura" in self.request.files:
            fileinfo = self.request.files["titulolicenciatura"][0]
            fname = fileinfo.filename
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            f = open("servidor/common/resources/images/foto_documentos/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()
            dicc_foto['titulolicenciatura'] = "/resources/images/foto_documentos/" + cname

        if "flcv" in self.request.files:
            fileinfo = self.request.files["flcv"][0]
            fname = fileinfo.filename
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            f = open("servidor/common/resources/images/foto_documentos/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()
            dicc_foto['flcv'] = "/resources/images/foto_documentos/" + cname

        if "otros" in self.request.files:
            fileinfo = self.request.files["otros"][0]
            fname = fileinfo.filename
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            f = open("servidor/common/resources/images/foto_documentos/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()
            dicc_foto['otros'] = "/resources/images/foto_documentos/" + cname

        dicc_foto['id'] = diccionary['id_documentos']
        list_doc.append(dicc_foto)

        diccionary['documentos'] = list_doc
        PersonalManager(self.db).update(diccionary)
        self.respond(success=True, message='Modificado correctamente.')


    def imprimirxls(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))

        cname = self.manager(self.db).personal_excel(diccionary['datos'])
        self.respond({'nombre': cname, 'url': 'resources/downloads/personal/' + cname}, True)
        self.db.close()

    def state(self):
        try:
            self.set_session()
            diccionary = json.loads(self.get_argument("object"))
            result = PersonalManager(self.db).state(diccionary['id'], diccionary['estado'], self.get_user_id(), self.request.remote_ip)

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
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))

        id = diccionary['id']
        state = diccionary['enabled']
        respuesta = PersonalManager(self.db).delete(id, self.get_user_id(), self.request.remote_ip)

        self.respond(success=True, message=respuesta)
        self.db.close()

    def report(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))

        pdf_codigo = PersonalManager(self.db).generar_codigo()

        html = PersonalManager(self.db).crear_pdf(diccionary)

        nombre = "Reporte_Personal_"+str(pdf_codigo)+".pdf"

        report.html_to_pdf(html, nombre)
        self.respond('/resources/downloads/' + nombre)

    def obtener_edad(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        result = PersonalManager(self.db).edad(diccionary['fechanacimiento'])

        self.respond(response=result ,
                     success=True,
                     message='')


    def buscar(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        indicted_object = self.manager(self.db).obtener_foto_x_id(diccionary['idPersonal'])

        if indicted_object:
            self.respond(response=indicted_object, success=True, message='Resultado Obtenido!')
        else:
            self.respond(response=None, success=False, message='No se encontraron resultados')
        self.db.close()