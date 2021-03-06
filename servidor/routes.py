from servidor.sistema.usuarios.login.controller import LoginController, LogoutController
from servidor.sistema.usuarios.usuario.controller import UsuarioController, ManualController
from servidor.sistema.usuarios.persona.controller import PersonaController
from servidor.sistema.usuarios.rol.controller import RolController
from servidor.sistema.usuarios.bitacora.controller import BitacoraController
from servidor.sistema.usuarios.ajuste.controller import AjusteController

from servidor.sistema.parametrizacion.categoria.controller import CategoriaController
from servidor.sistema.parametrizacion.civil.controller import CivilController
from servidor.sistema.parametrizacion.expedido.controller import ExpedidoController
from servidor.sistema.parametrizacion.grado.controller import GradoController
from servidor.sistema.parametrizacion.nacionalidad.controller import NacionalidadController
from servidor.sistema.parametrizacion.parentesco.controller import ParentescoController
from servidor.sistema.parametrizacion.retiro.controller import RetiroController
from servidor.sistema.parametrizacion.regimiento.controller import RegimientoController

from servidor.sistema.recursos_humanos.personal.controller import PersonalController
from servidor.sistema.recursos_humanos.cargo.controller import CargoController
from servidor.sistema.recursos_humanos.capacitacion.controller import CapacitacionController
from servidor.sistema.recursos_humanos.motivo.controller import MotivoController

from servidor.sistema.almacen.asignacion.controller import AsignacionController
from servidor.sistema.almacen.material.controller import MaterialController
from servidor.sistema.almacen.stock.controller import StockController
from servidor.sistema.almacen.tipomaterial.controller import TipoMaterialController
from servidor.sistema.almacen.almacen.controller import AlmacenController
from servidor.sistema.almacen.subalmacen.controller import SubAlmacenController
from servidor.sistema.almacen.descuento.controller import DescuentoController
from servidor.sistema.almacen.inventario.controller import InventarioController
from servidor.sistema.almacen.traspaso.controller import TraspasoController

from servidor.sistema.operador.cliente.controller import ClienteController
from servidor.sistema.operador.sancion.controller import SancionController
from servidor.sistema.operador.postulante.controller import PostulanteController
from servidor.sistema.operador.asistencia.controller import AsistenciaController


from servidor.main.controller import Index
from tornado.web import StaticFileHandler

import os


def get_routes(handler):
    routes = list()

    for route in handler.routes:
        routes.append((route, handler))

    return routes


def get_handlers():
    """Retorna una lista con las rutas, sus manejadores y datos extras."""
    handlers = list()

    # Principal
    handlers.append((r'/', Index))

    # Login
    handlers.append((r'/inicio', LoginController))
    handlers.append((r'/logout', LogoutController))

    # Usuarios
    handlers.append((r'/manual', ManualController))
    handlers.extend(get_routes(BitacoraController))
    handlers.extend(get_routes(RolController))
    handlers.extend(get_routes(UsuarioController))
    handlers.extend(get_routes(PersonaController))
    handlers.extend(get_routes(AjusteController))

    # Parametrizacion
    handlers.extend(get_routes(CategoriaController))
    handlers.extend(get_routes(CivilController))
    handlers.extend(get_routes(ExpedidoController))
    handlers.extend(get_routes(GradoController))
    handlers.extend(get_routes(NacionalidadController))
    handlers.extend(get_routes(ParentescoController))
    handlers.extend(get_routes(RetiroController))
    handlers.extend(get_routes(RegimientoController))

    # Recursos Humanos
    handlers.extend(get_routes(PersonalController))
    handlers.extend(get_routes(CargoController))
    handlers.extend(get_routes(CapacitacionController))
    handlers.extend(get_routes(MotivoController))

    # Almacen
    handlers.extend(get_routes(AsignacionController))
    handlers.extend(get_routes(MaterialController))
    handlers.extend(get_routes(InventarioController))
    handlers.extend(get_routes(TraspasoController))
    handlers.extend(get_routes(StockController))
    handlers.extend(get_routes(TipoMaterialController))
    handlers.extend(get_routes(AlmacenController))
    handlers.extend(get_routes(SubAlmacenController))
    handlers.extend(get_routes(DescuentoController))

    # Operador
    handlers.extend(get_routes(ClienteController))
    handlers.extend(get_routes(SancionController))
    handlers.extend(get_routes(AsistenciaController))
    handlers.extend(get_routes(PostulanteController))

    handlers.append((r'/resources/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'common', 'resources')}))

    # Recursos por submodulo
    handlers.append((r'/common/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'common', 'assets')}))
    handlers.append((r'/main/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'main', 'assets')}))
    handlers.append((r'/usuarios/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'sistema', 'usuarios')}))
    handlers.append((r'/negocio/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'sistema', 'negocio')}))
    handlers.append((r'/parametrizacion/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'sistema', 'parametrizacion')}))
    handlers.append((r'/recursos_humanos/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'sistema', 'recursos_humanos')}))
    handlers.append((r'/almacen/(.*)', StaticFileHandler,{'path': os.path.join(os.path.dirname(__file__), 'sistema', 'almacen')}))
    handlers.append((r'/operador/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'sistema', 'operador')}))

    return handlers
