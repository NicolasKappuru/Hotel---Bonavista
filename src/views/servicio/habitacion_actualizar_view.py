# views/servicio/habitacion_actualizar_view.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel,
    QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QComboBox
)
from PySide6.QtGui import QIntValidator
from db import get_conn
from datetime import date


class HabitacionActualizarView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window

        titulo = QLabel("Actualizar Estado de Habitación")
        titulo.setStyleSheet("font-size: 22px; font-weight: bold;")

        # Campo de búsqueda
        self.num_hab = QLineEdit()
        self.num_hab.setValidator(QIntValidator())
        self.num_hab.setPlaceholderText("Número de habitación")

        btn_buscar = QPushButton("Buscar")
        btn_buscar.clicked.connect(self.buscar)

        btn_back = QPushButton("Volver")
        btn_back.clicked.connect(self.main.ir_inicio_servicio)

        # Combo de estados
        self.combo_estado = QComboBox()
        self.combo_estado.setEnabled(False)

        btn_actualizar = QPushButton("Actualizar Estado")
        btn_actualizar.clicked.connect(self.actualizar)
        btn_actualizar.setEnabled(False)

        self.btn_actualizar = btn_actualizar  # Guardar referencia

        # Tabla
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(["Número", "Categoría", "Estado Actual"])
        self.tabla.setRowCount(0)

        h_busqueda = QHBoxLayout()
        h_busqueda.addWidget(QLabel("Número Habitación:"))
        h_busqueda.addWidget(self.num_hab)
        h_busqueda.addWidget(btn_buscar)

        h_estado = QHBoxLayout()
        h_estado.addWidget(QLabel("Nuevo Estado:"))
        h_estado.addWidget(self.combo_estado)
        h_estado.addWidget(btn_actualizar)

        h_botones = QHBoxLayout()
        h_botones.addWidget(btn_back)

        layout = QVBoxLayout()
        layout.addWidget(titulo)
        layout.addSpacing(15)
        layout.addLayout(h_busqueda)
        layout.addSpacing(10)
        layout.addWidget(self.tabla)
        layout.addSpacing(10)
        layout.addLayout(h_estado)
        layout.addLayout(h_botones)
        layout.addStretch()

        self.setLayout(layout)

        self.estados = {}    # estado_id: nombre_estado
        self.hab_actual = None  # para guardar la habitación cargada

    # ---------------------------------------------------
    #                 BUSCAR HABITACIÓN
    # ---------------------------------------------------
    def buscar(self):
        num = self.num_hab.text().strip()
        if not num:
            QMessageBox.warning(self, "Error", "Ingrese un número de habitación.")
            return

        conn = get_conn()
        cur = conn.cursor()

        try:
            # Obtener habitación
            cur.execute("""
                SELECT h.numero_habitacion, c.nombre_categoria, e.estado_id, e.nombre_estado
                FROM habitacion h
                JOIN categoria c ON h.categoria_id = c.categoria_id
                JOIN estado e ON h.estado_id = e.estado_id
                WHERE h.numero_habitacion = %s
            """, (num,))
            data = cur.fetchone()

            self.tabla.setRowCount(0)
            self.combo_estado.clear()
            self.combo_estado.setEnabled(False)
            self.btn_actualizar.setEnabled(False)

            if not data:
                QMessageBox.information(self, "Sin resultados", "La habitación no existe.")
                return

            # Llenar tabla
            self.tabla.setRowCount(1)
            self.tabla.setItem(0, 0, QTableWidgetItem(str(data[0])))
            self.tabla.setItem(0, 1, QTableWidgetItem(data[1]))
            self.tabla.setItem(0, 2, QTableWidgetItem(data[3]))

            # Guardar número de habitación
            self.hab_actual = data[0]
            estado_actual_id = data[2]

            # Cargar lista de estados disponibles
            cur.execute("SELECT estado_id, nombre_estado FROM estado")
            estados = cur.fetchall()

            self.estados = {eid: nombre for eid, nombre in estados}

            # Cargar en el combo
            for eid, nombre in estados:
                self.combo_estado.addItem(nombre, eid)

            # Seleccionar el estado actual
            idx = self.combo_estado.findData(estado_actual_id)
            if idx >= 0:
                self.combo_estado.setCurrentIndex(idx)

            self.combo_estado.setEnabled(True)
            self.btn_actualizar.setEnabled(True)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        finally:
            conn.close()

    # ---------------------------------------------------
    #                 ACTUALIZAR ESTADO
    # ---------------------------------------------------
    def actualizar(self):
        if not self.hab_actual:
            QMessageBox.warning(self, "Error", "Primero busque una habitación.")
            return

        nuevo_estado_id = self.combo_estado.currentData()

        conn = get_conn()
        cur = conn.cursor()

        try:
            # ============================================================
            # VALIDACIÓN GLOBAL
            # No permitir CAMBIAR el estado si existe una reserva activa
            # (fecha_salida >= hoy)
            # ============================================================
            cur.execute("""
                SELECT 1
                FROM reserva
                WHERE numero_habitacion = %s
                AND fecha_salida >= %s
                LIMIT 1
            """, (self.hab_actual, date.today()))

            if cur.fetchone():
                QMessageBox.warning(
                    self,
                    "No permitido",
                    "No puede cambiar el estado de esta habitación porque "
                    "tiene una reserva activa cuya fecha de salida aún no ha pasado."
                )
                return

            # ============================================================
            # ACTUALIZAR ESTADO (si pasó la validación)
            # ============================================================
            cur.execute("""
                UPDATE habitacion
                SET estado_id = %s
                WHERE numero_habitacion = %s
            """, (nuevo_estado_id, self.hab_actual))

            conn.commit()
            QMessageBox.information(self, "OK", "Estado actualizado correctamente.")

            # Reset UI
            self.hab_actual = None
            self.num_hab.clear()
            self.combo_estado.clear()
            self.combo_estado.setEnabled(False)
            self.btn_actualizar.setEnabled(False)
            self.tabla.setRowCount(0)

        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Error", str(e))
        finally:
            conn.close()