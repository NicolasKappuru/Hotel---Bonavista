# core/main_window.py
from PySide6.QtWidgets import QMainWindow, QStackedWidget

from views.recepcion.recepcion_home import RecepcionHome

from views.recepcion.cliente_insert_view import ClienteInsertView
from views.recepcion.cliente_update_view import ClienteUpdateView

from views.recepcion.reserva_insert_view import ReservaInsertView

from views.recepcion.reserva_list_view import ReservaListView
from views.recepcion.habitacion_dispo_view import HabitacionDispoView



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hotel Bonavista - Recepción")
        self.showMaximized() 
        
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Vistas del rol Recepción
        self.vista_recepcion_home = RecepcionHome(self)

        self.vista_cliente_insert = ClienteInsertView(self)
        self.vista_cliente_update = ClienteUpdateView(self)

        self.vista_reserva_insert = ReservaInsertView(self)

        self.vista_reservas = ReservaListView(self)
        self.vista_disponibilidad = HabitacionDispoView(self)

        self.stack.addWidget(self.vista_recepcion_home)  
        
        self.stack.addWidget(self.vista_cliente_insert)   
        self.stack.addWidget(self.vista_cliente_update)

        self.stack.addWidget(self.vista_reserva_insert)

        self.stack.addWidget(self.vista_reservas)        
        self.stack.addWidget(self.vista_disponibilidad) 

        self.ir_inicio_recepcion()

    # Métodos de navegación
    def ir_inicio_recepcion(self):
        self.stack.setCurrentWidget(self.vista_recepcion_home)

    def ir_cliente_insertar(self):
        self.stack.setCurrentWidget(self.vista_cliente_insert)

    def ir_cliente_actualizar(self):
        self.stack.setCurrentWidget(self.vista_cliente_update)

    def ir_reserva_insertar(self):
        self.stack.setCurrentWidget(self.vista_reserva_insert)

    def ir_reservas(self):
        self.stack.setCurrentWidget(self.vista_reservas)

    def ir_disponibilidad(self):
        self.stack.setCurrentWidget(self.vista_disponibilidad)
