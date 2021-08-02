from servidor.common.managers import SuperManager
from servidor.sistema.usuarios.bitacora.manager import BitacoraManager
from servidor.sistema.usuarios.usuario.manager import UsuarioManager
from servidor.sistema.usuarios.bitacora.model import Bitacora
from servidor.sistema.operador.cliente.model import Cliente,ClientePersonal
from servidor.sistema.operador.asistencia.model import TipoAusencia,Asistencia

from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import func, desc, asc

import pytz

global fecha_zona
fecha_zona = datetime.now(pytz.timezone('America/La_Paz'))


class ClienteManager(SuperManager):

    def __init__(self, db):
        super().__init__(Cliente, db)


    def listar_habilitados(self):
        return self.db.query(self.entity).filter(self.entity.estado).filter(self.entity.enabled).all()

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled).all()

    def list_all(self):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled))

    def get_all(self):
        items = self.db.query(self.entity).filter(self.entity.estado).filter(self.entity.enabled)
        return items

    def all_data_fecha(self, idu,fecha):
        privilegios = UsuarioManager(self.db).get_privileges(idu, '/cliente')
        datos = self.db.query(self.entity).filter(self.entity.enabled).order_by(asc(self.entity.id)).all()

        tipo_asistencia = self.db.query(TipoAusencia).filter(TipoAusencia.estado).filter(TipoAusencia.enabled).order_by(asc(TipoAusencia.id)).all()
        clientes = self.db.query(Cliente).filter(Cliente.estado).filter(Cliente.enabled).order_by(asc(Cliente.id)).all()

        lista_tipo = []
        for tipo in tipo_asistencia:
            lista_tipo.append(dict(id=tipo.id, codigo=tipo.codigo, nombre=tipo.nombre))

        lista_clientes = []
        for clie in clientes:
            lista_clientes.append(dict(id=clie.id, codigo=clie.codigo, nombre=clie.nombre))

        list = []

        cliente_personales = self.db.query(ClientePersonal).order_by(desc(ClientePersonal.id)).first()
        cont_id = cliente_personales.id
        for item in datos:
            is_active = item.estado
            disable = 'disabled' if 'cliente_update' not in privilegios else ''
            estado = 'Activo' if is_active else 'Inactivo'
            check = 'checked' if is_active else ''
            delete = 'cliente_delete' in privilegios

            lista_personal_dia = []
            lista_personal_noche = []
            lista_reemplazos = []

            for persona_ in item.personales:

                dicci = dict(id=persona_.id, fkpersona=persona_.fkpersonal,
                             fullname=persona_.personal.nombre + " " + persona_.personal.apellidop + " " + persona_.personal.apellidom,
                             fkasistencia=None,
                             color_asistencia=None,
                             fkreemplazo=None, observacion="")

                asistencia = self.db.query(Asistencia).filter(Asistencia.fkpersonal == persona_.fkpersonal) \
                    .filter(Asistencia.fkturno == persona_.fkturno) \
                    .filter(Asistencia.fkcliente == item.id) \
                    .filter(func.date(Asistencia.fechar) == func.date(fecha)).first()

                if persona_.fkturno == 1:

                    if asistencia:
                        dicci['fkasistencia'] = asistencia.fktipoausencia
                        dicci['color_asistencia'] = asistencia.tipoausencia.color
                        dicci['fkreemplazo'] = asistencia.fkreemplazo

                        if asistencia.fkreemplazo:
                            lista_reemplazos.append(dicci)
                    lista_personal_dia.append(dicci)

                else:

                    if asistencia:
                        dicci['fkasistencia'] = asistencia.fktipoausencia
                        dicci['color_asistencia'] = asistencia.tipoausencia.color
                        dicci['fkreemplazo'] = asistencia.fkreemplazo

                    lista_personal_noche.append(dicci)

            asistencia_reemplazos = self.db.query(Asistencia).filter(Asistencia.fkreemplazo == item.id) \
                .filter(func.date(Asistencia.fechar) == func.date(fecha)).all()

            cant_diurno = len(lista_personal_dia)
            cant_nocturno = len(lista_personal_noche)

            cont_id = cont_id + 1
            for persona_ in asistencia_reemplazos:

                if persona_.fktipoausencia == 6:
                    print(persona_.fktipoausencia)

                dicci = dict(id=cont_id, fkpersona=persona_.fkpersonal,
                             fullname=persona_.personal.nombre + " " + persona_.personal.apellidop + " " + persona_.personal.apellidom,
                             fkasistencia=persona_.fktipoausencia,
                             color_asistencia=persona_.tipoausencia.color,
                             fkreemplazo=None, observacion="Movil")

                cont_id = cont_id + 1
                if persona_.fkturno == 1:

                    lista_personal_dia.append(dicci)

                else:

                    lista_personal_noche.append(dicci)

            diccionario = item.get_dict()
            diccionario['estado'] = estado
            diccionario['check'] = check
            diccionario['disable'] = disable
            diccionario['delete'] = delete
            diccionario['tipo_asistencia'] = lista_tipo
            diccionario['clientes'] = lista_clientes
            diccionario['personal_dia'] = lista_personal_dia
            diccionario['personal_noche'] = lista_personal_noche
            diccionario['cantidad_personal_dia'] = cant_diurno
            diccionario['cantidad_personal_noche'] = cant_nocturno
            list.append(diccionario)

        return list

    def all_data(self, idu):
        privilegios = UsuarioManager(self.db).get_privileges(idu, '/cliente')
        datos = self.db.query(self.entity).filter(self.entity.enabled).order_by(asc(self.entity.id)).all()
        fecha = datetime.now(pytz.timezone('America/La_Paz'))

        tipo_asistencia = self.db.query(TipoAusencia).filter(TipoAusencia.estado).filter(TipoAusencia.enabled).all()
        clientes = self.db.query(Cliente).filter(Cliente.estado).filter(Cliente.enabled).all()

        lista_tipo = []
        for tipo in tipo_asistencia:
            lista_tipo.append(dict(id = tipo.id, codigo = tipo.codigo,nombre = tipo.nombre))

        lista_clientes = []
        for clie in clientes:
            lista_clientes.append(dict(id = clie.id, codigo = clie.codigo,nombre = clie.nombre))

        list = []

        cliente_personales = self.db.query(ClientePersonal).order_by(desc(ClientePersonal.id)).first()

        if cliente_personales:
            cont_id = cliente_personales.id
        else:
            cont_id = 0
        for item in datos:
            is_active = item.estado
            disable = 'disabled' if 'cliente_update' not in privilegios else ''
            estado = 'Activo' if is_active else 'Inactivo'
            check = 'checked' if is_active else ''
            delete = 'cliente_delete' in privilegios

            lista_personal_dia = []
            lista_personal_noche = []
            lista_reemplazos = []

            for persona_ in item.personales:

                dicci = dict(id = persona_.id,fkpersona=persona_.fkpersonal,
                                               fullname= persona_.personal.apellidop + " "+ persona_.personal.apellidom + " " + persona_.personal.nombre,
                                               fkasistencia= None,
                                               color_asistencia=None,
                                               fkreemplazo= None,observacion = "")

                asistencia = self.db.query(Asistencia).filter(Asistencia.fkpersonal == persona_.fkpersonal) \
                    .filter(Asistencia.fkturno == persona_.fkturno) \
                    .filter(Asistencia.fkcliente == item.id) \
                    .filter(func.date(Asistencia.fechar) == func.date(fecha)).first()

                if persona_.fkturno == 1:

                    if asistencia :
                        dicci['fkasistencia']= asistencia.fktipoausencia
                        dicci['color_asistencia'] = asistencia.tipoausencia.color
                        dicci['fkreemplazo'] = asistencia.fkreemplazo

                        if asistencia.fkreemplazo:
                            lista_reemplazos.append(dicci)
                    lista_personal_dia.append(dicci)

                else:

                    if asistencia:
                        dicci['fkasistencia'] = asistencia.fktipoausencia
                        dicci['color_asistencia'] = asistencia.tipoausencia.color
                        dicci['fkreemplazo'] = asistencia.fkreemplazo

                    lista_personal_noche.append(dicci)


            asistencia_reemplazos = self.db.query(Asistencia).filter(Asistencia.fkreemplazo == item.id) \
                .filter(func.date(Asistencia.fechar) == func.date(fecha)).all()


            cant_diurno = len(lista_personal_dia)
            cant_nocturno = len(lista_personal_noche)
            cont_id = cont_id + 1
            for persona_ in asistencia_reemplazos:

                if persona_.fktipoausencia == 6:
                    print (persona_.fktipoausencia)

                dicci = dict(id = cont_id,fkpersona=persona_.fkpersonal,
                                               fullname= persona_.personal.apellidop + " "+ persona_.personal.apellidom + " " + persona_.personal.nombre,
                                               fkasistencia= persona_.fktipoausencia,
                                               color_asistencia=persona_.tipoausencia.color,
                                               fkreemplazo= None,observacion = "Movil")

                cont_id = cont_id + 1
                if persona_.fkturno == 1:

                    lista_personal_dia.append(dicci)

                else:

                    lista_personal_noche.append(dicci)

            diccionario = item.get_dict()
            diccionario['estado'] = estado
            diccionario['check'] = check
            diccionario['disable'] = disable
            diccionario['delete'] = delete
            diccionario['tipo_asistencia'] = lista_tipo
            diccionario['clientes'] = lista_clientes
            diccionario['personal_dia'] = lista_personal_dia
            diccionario['personal_noche'] = lista_personal_noche
            diccionario['cantidad_personal_dia'] = cant_diurno
            diccionario['cantidad_personal_noche'] = cant_nocturno
            list.append(diccionario)

        return list

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registró cliente.", fecha=fecha, tabla="almacen_cliente", identificador=a.id)
        super().insert(b)
        return a

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modificó cliente.", fecha=fecha, tabla="almacen_cliente", identificador=a.id)
        super().insert(b)
        return a


    def state(self, id, estado, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        mensaje = "Habilitó cliente" if estado else "Deshabilitó cliente"
        x.estado = estado

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion=mensaje, fecha=fecha, tabla="almacen_cliente", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()
        return x

    def delete(self, id, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = False

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó cliente", fecha=fecha, tabla="almacen_cliente", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()



class ClienteTipoManager(SuperManager):

    def __init__(self, db):
        super().__init__(ClienteTipo, db)


    def get_all(self):
        items = self.db.query(self.entity).filter(self.entity.estado).filter(self.entity.enabled)
        return items



class ClienteTallaManager(SuperManager):

    def __init__(self, db):
        super().__init__(ClienteTalla, db)


    def get_all(self):
        items = self.db.query(self.entity).filter(self.entity.estado).filter(self.entity.enabled)
        return items

class ClienteColorManager(SuperManager):
    def __init__(self, db):
        super().__init__(ClienteColor, db)

    def get_all(self):
        items = self.db.query(self.entity).filter(self.entity.estado).filter(self.entity.enabled)
        return items