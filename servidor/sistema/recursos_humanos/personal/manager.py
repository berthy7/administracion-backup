from servidor.common.managers import SuperManager
from servidor.sistema.usuarios.bitacora.manager import BitacoraManager
from servidor.sistema.usuarios.usuario.manager import UsuarioManager
from servidor.sistema.usuarios.bitacora.model import Bitacora
from servidor.sistema.recursos_humanos.personal.model import Personal

from datetime import datetime

import pytz

global fecha_zona
fecha_zona = datetime.now(pytz.timezone('America/La_Paz'))

from random import *
import random

class PersonalManager(SuperManager):

    def __init__(self, db):
        super().__init__(Personal, db)


    def generar_codigo(self):
        longitud = 5
        valores = "0123456789"

        p = ""
        p = p.join([choice(valores) for i in range(longitud)])
        return p


    def obtener_x_id(self,idPersonal):
        return self.db.query(self.entity).filter(self.entity.id == idPersonal).first()

    def obtener_foto_x_id(self,idPersonal):
        x= self.db.query(self.entity).filter(self.entity.id == idPersonal).first()

        return dict(foto=x.foto)

    def crear_pdf(self, diccionario):

        persona = PersonalManager(self.db).obtener_x_id(diccionario['idPersonal'])
        var_categoriamotocicleta = "----"
        var_categoriavehiculo = "----"

        var_regimiento = "----"

        detalle_familiar = ""
        detalle_experiencia_laboral = ""
        detalle_estudios = ""
        detalle_complementos = ""

        if persona.fkcategoriavehiculo:
            var_categoriavehiculo = persona.categoriavehiculo.nombre

        if persona.fkcategoriamotocicleta:
            var_categoriamotocicleta = persona.categoriamotocicleta.nombre


        if persona.administrativos[0].fkregimiento:
            var_regimiento = persona.administrativos[0].regimiento.nombre

        else:
            var_regimiento = "----"



        for fami in persona.familiares:
            detalle_familiar = detalle_familiar + "" \
                                                  "<tr style='font-size: 12px; border: 0px; '>" \
                                                  "<td colspan='5' scope='colgroup'align='left'><font>" + str(fami.nombre) + "</font></td>" \
                                                   "<td colspan='5' scope='colgroup'align='left'><font>" + str(fami.celular) + "</font></td>" \
                                                    "<td colspan='5' scope='colgroup'align='left'><font>" + str(fami.parentesco.nombre) + "</font></td>" \
                                                              "</tr>"

        for expe in persona.experiencias:
            detalle_experiencia_laboral = detalle_experiencia_laboral + "" \
                                                                        "<tr style='font-size: 12px; border: 0px; '>" \
                                                                        "<td colspan='3' scope='colgroup'align='left'><font>" + str(
                expe.institucion) + "</font></td>" \
                                    "<td colspan='3' scope='colgroup'align='left'><font>" + str(
                expe.duracion) + "</font></td>" \
                                 "<td colspan='3' scope='colgroup'align='left'><font>" + str(
                expe.retiro.nombre) + "</font></td>" \
                                      "<td colspan='3' scope='colgroup'align='left'><font>" + str(
                expe.cargo) + "</font></td>" \
                              "<td colspan='3' scope='colgroup'align='left'><font>" + str(
                expe.referencia) + "</font></td>" \
                                   "<td colspan='3' scope='colgroup'align='left'><font>" + str(
                expe.telefono) + "</font></td>" \
                                 "</tr>"

        for estu in persona.estudios:
            detalle_estudios = detalle_estudios + "" \
                                                  "<tr style='font-size: 12px; border: 0px; '>" \
                                                  "<td colspan='5' scope='colgroup'align='left'><font>" + str(
                estu.institucion) + "</font></td>" \
                                    "<td colspan='5' scope='colgroup'align='left'><font>" + str(
                estu.grado.nombre) + "</font></td>" \
                                     "<td colspan='5' scope='colgroup'align='left'><font>" + str(
                estu.egreso) + "</font></td>" \
                               "</tr>"

        for comple in persona.complementos:
            detalle_complementos = detalle_complementos + "" \
                                                          "<tr style='font-size: 12px; border: 0px; '>" \
                                                          "<td colspan='5' scope='colgroup'align='left'><font>" + str(
                comple.estudio) + "</font></td>" \
                                  "<td colspan='5' scope='colgroup'align='left'><font></font></td>" \
                                       "</tr>"

        if persona.documentos[0].ci:
            foto1x = "<tr>" \
                     "<td width='100%' colspan='20' align='center' ><strong>CEDULAR DE IDENTIDAD</strong><img src='/common" + \
                     persona.documentos[0].ci + "' width='auto' height='500'></td>" \
                                                "</tr>"
        else:
            foto1x = "<tr>" \
                     "<td width='100%' colspan='20' align='center' ><strong>CEDULAR DE IDENTIDAD</strong></td>" \
                     "</tr>"

        if persona.documentos[0].libretamilitar:
            foto2x = "<tr>" \
                     "<td width='100%' colspan='20' align='center' ><strong>LIBRETA DE SERVICIO MILITAR</strong><img src='/common" + \
                     persona.documentos[0].libretamilitar + "' width='auto' height='500'></td>" \
                                                            "</tr>"
        else:
            foto2x = "<tr>" \
                     "<td width='100%' colspan='20' align='center' ><strong>LIBRETA DE SERVICIO MILITAR</strong></td>" \
                     "</tr>"

        if persona.documentos[0].titulobachiller:
            foto3x = "<tr>" \
                     "<td width='100%' colspan='20' align='center' ><strong>TITULO DE BACHILLER</strong><img src='/common" + \
                     persona.documentos[0].titulobachiller + "' width='auto' height='500'></td>" \
                                                             "</tr>"
        else:
            foto3x = "<tr>" \
                     "<td width='100%' colspan='20' align='center' ><strong>TITULO DE BACHILLER</strong></td>" \
                     "</tr>"

        if persona.documentos[0].titulotecnico:
            foto4x = "<tr>" \
                     "<td width='100%' colspan='20' align='center' ><strong>TITULO TECNICO</strong><img src='/common" + \
                     persona.documentos[0].titulotecnico + "' width='auto' height='500'></td>" \
                                                           "</tr>"
        else:
            foto4x = "<tr>" \
                     "<td width='100%' colspan='20' align='center' ><strong>TITULO TECNICO</strong></td>" \
                     "</tr>"

        if persona.documentos[0].titulolicenciatura:
            foto5x = "<tr>" \
                     "<td width='100%' colspan='20' align='center' ><strong>TITULO DE LICENCIATURA</strong><img src='/common" + \
                     persona.documentos[0].titulolicenciatura + "' width='auto' height='500'></td>" \
                                                                "</tr>"
        else:
            foto5x = "<tr>" \
                     "<td width='100%' colspan='20' align='center' ><strong>TITULO DE LICENCIATURA</strong></td>" \
                     "</tr>"

        if persona.documentos[0].flcn:
            foto6x = "<tr>" \
                     "<td width='100%' colspan='20' align='center' ><strong>FLCN</strong><img src='/common" + \
                     persona.documentos[0].flcn + "' width='auto' height='500'></td>" \
                                                  "</tr>"
        else:
            foto6x = "<tr>" \
                     "<td width='100%' colspan='20' align='center' ><strong>FLCN</strong></td>" \
                     "</tr>"

        if persona.documentos[0].flcc:
            foto7x = "<tr>" \
                     "<td width='100%' colspan='20' align='center' ><strong>FELCC</strong><img src='/common" + \
                     persona.documentos[0].flcc + "' width='auto' height='500'></td>" \
                                                  "</tr>"
        else:
            foto7x = "<tr>" \
                     "<td width='100%' colspan='20' align='center' ><strong>FELCC</strong></td>" \
                     "</tr>"

        if persona.documentos[0].luzagua:
            foto8x = "<tr>" \
                     "<td width='100%' colspan='20' align='center' ><strong>LUZ O AGUA</strong><img src='/common" + \
                     persona.documentos[0].luzagua + "' width='auto' height='500'></td>" \
                                                     "</tr>"
        else:
            foto8x = "<tr>" \
                     "<td width='100%' colspan='20' align='center' ><strong>LUZ O AGUA</strong></td>" \
                     "</tr>"

        if persona.documentos[0].certificadonacimiento:
            foto9x = "<tr>" \
                     "<td width='100%' colspan='20' align='center' ><strong>CERTIFICADO DE NACIMIENTO</strong><img src='/common" + \
                     persona.documentos[0].certificadonacimiento + "' width='auto' height='500'></td>" \
                                                                   "</tr>"
        else:
            foto9x = "<tr>" \
                     "<td width='100%' colspan='20' align='center' ><strong>CERTIFICADO DE NACIMIENTO</strong></td>" \
                     "</tr>"

        if persona.documentos[0].flcv:
            foto10x = "<tr>" \
                      "<td width='100%' colspan='20' align='center' ><strong>FLCV</strong><img src='/common" + \
                      persona.documentos[0].flcv + "' width='auto' height='500'></td>" \
                                                   "</tr>"
        else:
            foto10x = "<tr>" \
                      "<td width='100%' colspan='20' align='center' ><strong>FLCV</strong></td>" \
                      "</tr>"

        if persona.documentos[0].otros:
            foto11x = "<tr>" \
                      "<td width='100%' colspan='20' align='center' ><strong>OTROS</strong><img src='/common" + \
                      persona.documentos[0].otros + "' width='auto' height='500'></td>" \
                                                    "</tr>"
        else:
            foto11x = "<tr>" \
                      "<td width='100%' colspan='20' align='center' ><strong>OTROS</strong></td>" \
                      "</tr>"

        logoempresa = "/resources/iconos/logo.png"

        html = "" \
               "<meta http-equiv='Content-Type' content='text/html'; charset='utf-8' />" \
               "<style>" \
               ".border-own { border-left: 0px; border-right: 0px; }" \
               ".border-own-l { border-right: 0px; }" \
               ".border-own-r { border-left: 0px; }" \
               "@page {size: letter portrait; margin: 1cm; @frame footer_frame {-pdf-frame-content: footer_content; left: 50pt; width: 512pt; top: 772pt; height: 20pt; }}" \
               "</style>" \

        html += "" \
                "<table style='padding: 4px; border: 0px solid grey' width='100%'>" \
                "<tr style='font-size: 12px; border: 0px; '>" \
                "<td colspan='5' style='border-right: 0px solid grey ' scope='colgroup'align='left'><img src='/common" + logoempresa + "' width='auto' height='75'></td>" \
                "<td colspan='12' scope='colgroup'align='left'><font></font></td>" \
                "<td colspan='5' style='border-left: 0px solid grey ' scope='colgroup'align='center'><img src='/common" + str(persona.foto) + "' width='auto' height='75'></td>" \
              "</tr>" \
                      "</table>" \
                      "<table style='padding: 4px; border: 1px solid grey' width='100%'>" \
                      "<tr color='#ffffff' >" \
                      "<th colspan='22' scope='colgroup' align='left' style='background-color: #DC3131; font-size=4; color: white; margin-top: 4px'>REPORTE DE PERSONAL</th>" \
                      "</tr>" \
                      "<tr style='font-size: 12px; border: 0px; '>" \
                      "<td colspan='5' style='border-right: 1px solid grey ' scope='colgroup'align='left'><strong>Nombres y Apellidos: </strong></td>" \
                      "<td colspan='12' scope='colgroup'align='left'><font>" + str(
                    persona.fullname) + "</font></td>" \
                                        "</tr>" \
                                        "<tr style='font-size: 12px; border: 0px; '>" \
                                        "<td colspan='5' style='border-right: 1px solid grey ' scope='colgroup'align='left'><strong>DNI: </strong></td>" \
                                        "<td colspan='12' scope='colgroup'align='left'><font>" + str(
                    persona.ci) + " " + persona.expedido.nombre + "</font></td>" \
                                                                  "</tr>" \
                                                                  "<tr style='font-size: 12px; border: 0px; '>" \
                                                                  "<td colspan='5' style='border-right: 1px solid grey ' scope='colgroup'align='left'><strong>Nacionalidad: </strong></td>" \
                                                                  "<td colspan='12' scope='colgroup'align='left'><font>" + str(
                    persona.nacionalidad.nombre) + "</font></td>" \
                                                   "</tr>" \
                                                   "<tr style='font-size: 12px; border: 0px; '>" \
                                                   "<td colspan='5' style='border-right: 1px solid grey ' scope='colgroup'align='left'><strong>Fecha Nacimiento: </strong></td>" \
                                                   "<td colspan='12' scope='colgroup'align='left'><font>" + str(
                    persona.fechanacimiento.strftime('%d/%m/%Y')) + "</font></td>" \
                                                                    "</tr>" \
                                                                    "<tr style='font-size: 12px; border: 0px; '>" \
                                                                    "<td colspan='5' style='border-right: 1px solid grey ' scope='colgroup'align='left'><strong>Licencia Vehiculo: </strong></td>" \
                                                                    "<td colspan='5' scope='colgroup'align='left'><font>" + str(
                    persona.licenciavehiculo) + "</font></td>" \
                                                "<td colspan='5' style='border-right: 0px solid grey ' scope='colgroup'align='left'><strong>Categoria: </strong>" + var_categoriavehiculo + "</td>" \
                                                              "</tr>" \
                                                              "<tr style='font-size: 12px; border: 0px; '>" \
                                                              "<td colspan='5' style='border-right: 1px solid grey ' scope='colgroup'align='left'><strong>Licencia Motocicleta: </strong></td>" \
                                                              "<td colspan='5' scope='colgroup'align='left'><font>" + str(
                    persona.licenciamotocicleta) + "</font></td>" \
                                                   "<td colspan='5' style='border-right: 0px solid grey ' scope='colgroup'align='left'><strong>Categoria: </strong>" + var_categoriamotocicleta + "</td>" \
                                          "</tr>" \
                                          "<tr style='font-size: 12px; border: 0px; '>" \
                                          "<td colspan='5' style='border-right: 1px solid grey ' scope='colgroup'align='left'><strong>Domicilio: </strong></td>" \
                                          "<td colspan='12' scope='colgroup'align='left'><font>" + str(
                    persona.domicilio) + "</font></td>" \
                                         "</tr>" \
                                         "<tr style='font-size: 12px; border: 0px; '>" \
                                         "<td colspan='5' style='border-right: 1px solid grey ' scope='colgroup'align='left'><strong>Nro. Celular: </strong></td>" \
                                         "<td colspan='12' scope='colgroup'align='left'><font>" + str(
                    persona.telefono) + "</font></td>" \
                                        "</tr>" \
                                        "<tr style='font-size: 12px; border: 0px; '>" \
                                        "<td colspan='5' style='border-right: 1px solid grey ' scope='colgroup'align='left'><strong>Estado Civil: </strong></td>" \
                                        "<td colspan='12' scope='colgroup'align='left'><font>" + str(
                    persona.civil.nombre) + "</font></td>" \
                                            "</tr>" \
                                            "<tr style='font-size: 12px; border: 0px; '>" \
                                            "<td colspan='5' style='border-right: 1px solid grey ' scope='colgroup'align='left'><strong>Cargo: </strong></td>" \
                                            "<td colspan='12' scope='colgroup'align='left'><font>" + str(
            persona.cargo.nombre) + "</font></td>" \
                                    "</tr>" \
                                    "</table>" \
                                            "<table style='padding: 4px; border: 1px solid grey' width='100%'>" \
                                            "<tr style='font-size: 12px; border: 0px; '>" \
                                            "<td colspan='5' style='border-right: 0px solid grey ' scope='colgroup'align='left'><strong>Servicio Militar</strong></td>" \
                                            "<td colspan='5' style='border-right: 0px solid grey ' scope='colgroup'align='left'><strong>Nº de Libreta</strong></td>" \
                                            "<td colspan='5' style='border-right: 0px solid grey ' scope='colgroup'align='left'><strong>Expedido en:</strong></td>" \
                                            "</tr>" \
                                            "<tr style='font-size: 12px; border: 0px; '>" \
                                            "<td colspan='5' scope='colgroup'align='left'><font>" + str(persona.administrativos[0].serviciomilitar) + "</font></td>" \
                                            "<td colspan='5' scope='colgroup'align='left'><font>" + str(persona.administrativos[0].nrolibreta) + "</font></td>" \
                                            "<td colspan='5' scope='colgroup'align='left'><font>" + var_regimiento + "</font></td>" \
                   "</tr>" \
                   "</table>" \
                   "<table style='padding: 4px; border: 1px solid grey' width='100%'>" \
                   "<tr style='font-size: 12px; border: 0px; '>" \
                   "<td colspan='5' style='border-right: 0px solid grey ' scope='colgroup'align='left'><strong>Familiar de referencia: </strong></td>" \
                   "<td colspan='12' scope='colgroup'align='left'><font></font></td>" \
                   "</tr>" \
                   "<tr style='font-size: 12px; border: 0px; '>" \
                   "<td colspan='5' style='border-right: 0px solid grey ' scope='colgroup'align='left'><strong>Nombre</strong></td>" \
                   "<td colspan='5' style='border-right: 0px solid grey ' scope='colgroup'align='left'><strong>Celular</strong></td>" \
                   "<td colspan='5' style='border-right: 0px solid grey ' scope='colgroup'align='left'><strong>Parentesco</strong></td>" \
                   "</tr>" \
                   "" + detalle_familiar + "" \
                   "</table>" \
                   "<table style='padding: 4px; border: 1px solid grey' width='100%'>" \
                   "<tr style='font-size: 12px; border: 0px; '>" \
                   "<td colspan='5' style='border-right: 0px solid grey ' scope='colgroup'align='left'><strong>Experiencia Laboral: </strong></td>" \
                   "<td colspan='12' scope='colgroup'align='left'><font></font></td>" \
                   "</tr>" \
                   "<tr style='font-size: 12px; border: 0px; '>" \
                   "<td colspan='3' style='border-right: 0px solid grey ' scope='colgroup'align='left'><strong>Institucion</strong></td>" \
                   "<td colspan='3' style='border-right: 0px solid grey ' scope='colgroup'align='left'><strong>Duracion</strong></td>" \
                   "<td colspan='3' style='border-right: 0px solid grey ' scope='colgroup'align='left'><strong>Motivo de retiro</strong></td>" \
                   "<td colspan='3' style='border-right: 0px solid grey ' scope='colgroup'align='left'><strong>Cargo</strong></td>" \
                   "<td colspan='3' style='border-right: 0px solid grey ' scope='colgroup'align='left'><strong>Nombre refencia</strong></td>" \
                   "<td colspan='3' style='border-right: 0px solid grey ' scope='colgroup'align='left'><strong>Telefono</strong></td>" \
                   "</tr>" \
                   "" + detalle_experiencia_laboral + "" \
                  "</table>" \
                  "<table style='padding: 4px; border: 1px solid grey' width='100%'>" \
                  "<tr style='font-size: 12px; border: 0px; '>" \
                  "<td colspan='5' style='border-right: 0px solid grey ' scope='colgroup'align='left'><strong>Estudios Realizados: </strong></td>" \
                  "<td colspan='12' scope='colgroup'align='left'><font></font></td>" \
                  "</tr>" \
                  "<tr style='font-size: 12px; border: 0px; '>" \
                  "<td colspan='5' style='border-right: 0px solid grey ' scope='colgroup'align='left'><strong>Institucion</strong></td>" \
                  "<td colspan='5' style='border-right: 0px solid grey ' scope='colgroup'align='left'><strong>Grado</strong></td>" \
                  "<td colspan='5' style='border-right: 0px solid grey ' scope='colgroup'align='left'><strong>Egreso</strong></td>" \
                  "</tr>" \
                  "" + detalle_estudios + "" \
                  "<tr style='font-size: 12px; border: 0px; '>" \
                  "<td colspan='5' style='border-right: 0px solid grey ' scope='colgroup'align='left'><strong>Complementos: </strong></td>" \
                  "<td colspan='12' scope='colgroup'align='left'><font></font></td>" \
                  "</tr>" \
                  "<tr style='font-size: 12px; border: 0px; '>" \
                  "<td colspan='5' style='border-right: 0px solid grey ' scope='colgroup'align='left'><strong>Estudio</strong></td>" \
                  "<td colspan='5' style='border-right: 0px solid grey ' scope='colgroup'align='left'><strong>Grado</strong></td>" \
                  "</tr>" \
                  "" + detalle_complementos + "" \
                                          "</table>" \
                  "</br>"
        html += "<table style='padding: 4px; border: 1px solid grey' width='100%'>" \
                "" + foto1x + "" \
                              "" + foto2x + "" \
                                            "" + foto3x + "" \
                                                          "" + foto4x + "" \
                                                                        "" + foto5x + "" \
                                                                                      "" + foto6x + "" \
                                                                                                    "" + foto7x + "" \
                                                                                                                  "" + foto8x + "" \
                                                                                                                                "" + foto9x + "" \
                                                                                                                                              "" + foto10x + "" \
                                                                                                                                                             "" + foto11x + "" \
                                                                                                                                                                            "</table>"

        return html

    def listar_habilitados(self):
        return self.db.query(self.entity).filter(self.entity.estado).filter(self.entity.enabled).all()

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled).all()

    def list_all(self):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled))

    def get_all(self):
        items = self.db.query(self.entity).filter(self.entity.estado).filter(self.entity.enabled)
        return items

    def get_all_solo_foto(self):
        items = self.db.query(self.entity).filter(self.entity.estado).filter(self.entity.enabled).filter(self.entity.foto != None)
        return items

    def all_data(self, idu):
        privilegios = UsuarioManager(self.db).get_privileges(idu, '/personal')
        datos = self.db.query(self.entity).filter(self.entity.enabled).all()
        list = []

        for item in datos:
            is_active = item.estado
            disable = 'disabled' if 'personal_update' not in privilegios else ''
            estado = 'Activo' if is_active else 'Inactivo'
            check = 'checked' if is_active else ''
            delete = 'personal_delete' in privilegios

            diccionario = item.get_dict()
            diccionario['estado'] = estado
            diccionario['check'] = check
            diccionario['disable'] = disable
            diccionario['delete'] = delete
            diccionario['fechar'] = item.fechar.strftime('%d/%m/%Y')
            diccionario['fullname'] = item.fullname
            diccionario['cargo'] = item.cargo.nombre

            list.append(diccionario)

        return list

    def insert(self, diccionary):

        if diccionary['fkcategoriamotocicleta'] == '':
            diccionary['fkcategoriamotocicleta'] = None

        if diccionary['fkcategoriavehiculo'] == '':
            diccionary['fkcategoriavehiculo'] = None

        if diccionary['administrativos'][0]['fkregimiento'] == "":
            diccionary['administrativos'][0]['fkregimiento']= None



        objeto = PersonalManager(self.db).entity(**diccionary)
        objeto.fechanacimiento = datetime.strptime(objeto.fechanacimiento, '%d/%m/%Y')


        fecha = BitacoraManager(self.db).fecha_actual()

        objeto.fechar = fecha

        a = super().insert(objeto)

        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Personal.", fecha=fecha,tabla="personal", identificador=a.id)
        super().insert(b)

        return a

    def update(self, diccionary):


        objeto = PersonalManager(self.db).entity(**diccionary)
        fecha = BitacoraManager(self.db).fecha_actual()
        objeto.fechanacimiento = datetime.strptime(objeto.fechanacimiento, '%d/%m/%Y')


        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Personal.", fecha=fecha,tabla="personal", identificador=a.id)
        super().insert(b)


        return a

    def state(self, id, estado, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        mensaje = "Habilitó personal" if estado else "Deshabilitó personal"
        x.estado = estado

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion=mensaje, fecha=fecha, tabla="recursos_humanos_personal", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()
        return x

    def delete(self, id, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = False

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó personal", fecha=fecha, tabla="recursos_humanos_personal", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()


    def edad(self, fechanacimiento):
        fechanacimiento = datetime.strptime(fechanacimiento, '%d/%m/%Y')
        fecha = datetime.now(pytz.timezone('America/La_Paz'))

        diff = fecha.year - fechanacimiento.year

        diff -= ((fecha.month, fecha.day) < (fechanacimiento.month, fechanacimiento.day))

        return diff


    def actualizar_foto(self, id, foto,user,ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).first()

        x.foto = foto

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Actualizacion de foto", fecha=fecha, tabla="recursos_humanos_personal", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()
        return x