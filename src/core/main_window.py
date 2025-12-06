# core/main_window.py
from PySide6.QtWidgets import QMainWindow, QStackedWidget

# --- Recepción ---
from views.recepcion.recepcion_home import RecepcionHome
from views.recepcion.cliente_insert_view import ClienteInsertView
from views.recepcion.cliente_update_view import ClienteUpdateView
from views.recepcion.cliente_consult_view import ClienteHuespedView
from views.recepcion.reserva_insert_view import ReservaInsertView
from views.recepcion.reserva_update_view import ReservaUpdateView
from views.recepcion.reserva_list_view import ReservaListView
from views.recepcion.habitacion_dispo_view import HabitacionDispoView

# --- Servicios ---
from views.servicio.servicio_home import ServicioHome
from views.servicio.habitacion_consultar_view import HabitacionConsultarView
from views.servicio.habitacion_actualizar_view import HabitacionActualizarView
from views.servicio.consultar_servicios_view import ServiciosConsultarView
from views.servicio.servicio_asignar_view import ServicioAsignarView

# --- Administración ---
from views.administracion.administracion_home import AdministracionHome
from views.administracion.empleado_insert_view import EmpleadoInsertView
from views.administracion.empleado_update_view import EmpleadoUpdateView
from views.administracion.empleado_consultar_view import EmpleadoConsultarView
from views.administracion.empleado_delete_view import EmpleadoDeleteView
from views.administracion.servicio_actualizar_view import ServiciosActualizarView
from views.administracion.habitaciones_mas_reservadas_view import HabitacionesMasReservadasView
from views.administracion.servicios_mas_solicitados_view import ServiciosMasSolicitadosView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hotel Bonavista - Servicios")
        self.showMaximized()

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # ===========================
        #        RECEPCIÓN
        # ===========================
        self.vista_recepcion_home = RecepcionHome(self)
        self.vista_cliente_insert = ClienteInsertView(self)
        self.vista_cliente_update = ClienteUpdateView(self)
        self.vista_cliente_consult = ClienteHuespedView(self)
        self.vista_reserva_insert = ReservaInsertView(self)
        self.vista_reserva_update = ReservaUpdateView(self)
        self.vista_reservas = ReservaListView(self)
        self.vista_disponibilidad = HabitacionDispoView(self)

        # ===========================
        #        SERVICIOS
        # ===========================
        self.vista_servicio_home = ServicioHome(self)
        self.vista_habitacion_consultar = HabitacionConsultarView(self)
        self.vista_habitacion_actualizar = HabitacionActualizarView(self)
        self.vista_servicios_consultar = ServiciosConsultarView(self)
        self.vista_servicio_asignar = ServicioAsignarView(self)

        # ===========================
        #    ADMINISTRACIÓN
        # ===========================
        self.vista_admin_home = AdministracionHome(self)
        self.vista_empleado_insert = EmpleadoInsertView(self)
        self.vista_empleado_update = EmpleadoUpdateView(self)
        self.vista_empleado_consultar = EmpleadoConsultarView(self)
        self.vista_empleado_eliminar = EmpleadoDeleteView(self)
        self.vista_servicios_actualizar = ServiciosActualizarView(self)
        self.vista_habitaciones_mas_reservadas = HabitacionesMasReservadasView(self)
        self.vista_servicios_mas_solicitados = ServiciosMasSolicitadosView(self)

        # Agregar al stack
        self.stack.addWidget(self.vista_recepcion_home)
        self.stack.addWidget(self.vista_cliente_insert)
        self.stack.addWidget(self.vista_cliente_update)
        self.stack.addWidget(self.vista_cliente_consult)
        self.stack.addWidget(self.vista_reserva_insert)
        self.stack.addWidget(self.vista_reserva_update)
        self.stack.addWidget(self.vista_reservas)
        self.stack.addWidget(self.vista_disponibilidad)

        self.stack.addWidget(self.vista_servicio_home)
        self.stack.addWidget(self.vista_habitacion_consultar)
        self.stack.addWidget(self.vista_habitacion_actualizar)
        self.stack.addWidget(self.vista_servicios_consultar)
        self.stack.addWidget(self.vista_servicio_asignar)

        self.stack.addWidget(self.vista_admin_home)
        self.stack.addWidget(self.vista_empleado_insert)
        self.stack.addWidget(self.vista_empleado_update)
        self.stack.addWidget(self.vista_empleado_consultar)
        self.stack.addWidget(self.vista_empleado_eliminar)
        self.stack.addWidget(self.vista_servicios_actualizar)
        self.stack.addWidget(self.vista_habitaciones_mas_reservadas)
        self.stack.addWidget(self.vista_servicios_mas_solicitados)

        # Arrancamos ahora en SERVICIO
        #self.ir_inicio_recepcion()
        #self.ir_inicio_servicio()
        self.ir_inicio_administracion()

    # ===========================
    #      NAVEGACIÓN RECEPCIÓN
    # ===========================

    def ir_inicio_recepcion(self):
        self.stack.setCurrentWidget(self.vista_recepcion_home)

    def ir_cliente_insertar(self):
        self.stack.setCurrentWidget(self.vista_cliente_insert)

    def ir_cliente_actualizar(self):
        self.stack.setCurrentWidget(self.vista_cliente_update)

    def ir_cliente_consultar(self):
        self.stack.setCurrentWidget(self.vista_cliente_consult)

    def ir_reserva_insertar(self):
        self.stack.setCurrentWidget(self.vista_reserva_insert)

    def ir_reserva_actualizar(self):
        self.stack.setCurrentWidget(self.vista_reserva_update)

    def ir_reservas(self):
        self.stack.setCurrentWidget(self.vista_reservas)

    def ir_disponibilidad(self):
        self.stack.setCurrentWidget(self.vista_disponibilidad)

    # ===========================
    #      NAVEGACIÓN SERVICIOS
    # ===========================

    def ir_inicio_servicio(self):
        self.stack.setCurrentWidget(self.vista_servicio_home)

    def ir_habitacion_consultar(self):
        self.stack.setCurrentWidget(self.vista_habitacion_consultar)

    def ir_habitacion_actualizar(self):
        self.stack.setCurrentWidget(self.vista_habitacion_actualizar)

    def ir_servicios_consultar(self):
        self.stack.setCurrentWidget(self.vista_servicios_consultar)

    def ir_servicio_asignar(self):
        self.stack.setCurrentWidget(self.vista_servicio_asignar)


    # ===========================
    #   NAVEGACIÓN ADMINISTRACIÓN
    # ===========================
    def ir_admin_home(self):
        self.stack.setCurrentWidget(self.vista_admin_home)

    def ir_inicio_administracion(self):
        self.stack.setCurrentWidget(self.vista_admin_home)

    def ir_empleado_insertar(self):
        self.stack.setCurrentWidget(self.vista_empleado_insert)
   
    def ir_empleado_actualizar(self):
        self.stack.setCurrentWidget(self.vista_empleado_update)
   
    def ir_empleado_consultar(self):
        self.stack.setCurrentWidget(self.vista_empleado_consultar)
    
    def ir_empleado_eliminar(self):
        self.stack.setCurrentWidget(self.vista_empleado_eliminar)
    
    def ir_servicios_actualizar(self):
        self.stack.setCurrentWidget(self.vista_servicios_actualizar)
    
    def ir_habitaciones_mas_reservadas(self):
        self.stack.setCurrentWidget(self.vista_habitaciones_mas_reservadas)

    def ir_servicios_mas_solicitados(self):
        self.stack.setCurrentWidget(self.vista_servicios_mas_solicitados)