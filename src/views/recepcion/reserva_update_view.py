# views/recepcion/reserva_update_view.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QLabel,
    QPushButton, QMessageBox, QComboBox, QDateEdit
)
from PySide6.QtGui import QIntValidator
from PySide6.QtCore import QDate
from db import get_conn


class ReservaUpdateView(QWidget):

    def __init__(self, main_window=None):
        super().__init__(main_window)
        self.main = main_window
        self.setWindowTitle("Actualizar Reserva")
        self.resize(900, 600)

        # Campos
        self.reserva_id = QLineEdit()
        self.reserva_id.setValidator(QIntValidator())

        self.tipo_doc = QLineEdit()
        self.tipo_doc.setReadOnly(True)

        self.num_doc = QLineEdit()
        self.num_doc.setReadOnly(True)

        self.fecha_llegada = QDateEdit()
        self.fecha_llegada.setDisplayFormat("yyyy-MM-dd")
        self.fecha_llegada.setReadOnly(True)

        self.fecha_salida = QDateEdit()
        self.fecha_salida.setDisplayFormat("yyyy-MM-dd")
        self.fecha_salida.setCalendarPopup(True)

        self.tiempo_cancel = QLineEdit()
        self.tiempo_cancel.setValidator(QIntValidator())

        self.num_hab = QLineEdit()
        self.num_hab.setValidator(QIntValidator())

        # Botones
        self.btn_buscar = QPushButton("Buscar")
        self.btn_buscar.clicked.connect(self.buscar_reserva)

        self.btn_actualizar = QPushButton("Actualizar")
        self.btn_actualizar.clicked.connect(self.actualizar)
        self.btn_actualizar.setEnabled(False)

        self.btn_volver = QPushButton("Volver")
        if self.main:
            self.btn_volver.clicked.connect(self.main.ir_inicio_recepcion)
        else:
            self.btn_volver.clicked.connect(self.close)

        # Layout formulario
        form = QFormLayout()
        form.addRow("ID Reserva:", self.reserva_id)
        form.addRow("Tipo Doc:", self.tipo_doc)
        form.addRow("Número Doc:", self.num_doc)
        form.addRow("Fecha Llegada:", self.fecha_llegada)
        form.addRow("Fecha Salida:", self.fecha_salida)
        form.addRow("Tiempo Máx Cancelación:", self.tiempo_cancel)
        form.addRow("Número Habitación:", self.num_hab)

        h_consulta = QHBoxLayout()
        h_consulta.addWidget(self.btn_buscar)

        h_buttons = QHBoxLayout()
        h_buttons.addWidget(self.btn_actualizar)
        h_buttons.addWidget(self.btn_volver)

        layout = QVBoxLayout()
        layout.addLayout(h_consulta)
        layout.addLayout(form)
        layout.addLayout(h_buttons)
        layout.addStretch()
        self.setLayout(layout)

    # ---------------------------------
    #      Buscar reserva por ID
    # ---------------------------------
    def buscar_reserva(self):
        rid = self.reserva_id.text().strip()
        if not rid:
            QMessageBox.warning(self, "Error", "Ingrese un ID de reserva.")
            return

        conn = get_conn()
        cur = conn.cursor()

        try:
            cur.execute("""
                SELECT reserva_id, tiempo_max_cancelacion,
                       fecha_llegada, fecha_salida,
                       tipo_documento, numero_documento,
                       numero_habitacion
                FROM reserva
                WHERE reserva_id = %s
            """, (rid,))
            r = cur.fetchone()

            if not r:
                QMessageBox.information(self, "No encontrado", "No existe una reserva con ese ID.")
                return

            self.tiempo_cancel.setText(str(r[1]))
            self.fecha_llegada.setDate(r[2])
            self.fecha_salida.setDate(r[3])
            self.tipo_doc.setText(r[4])
            self.num_doc.setText(r[5])
            self.num_hab.setText(str(r[6]))

            self.old_habitacion = r[6]  # para comparación
            self.btn_actualizar.setEnabled(True)
            QMessageBox.information(self, "Cargado", "Reserva cargada correctamente.")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        finally:
            conn.close()

    # ---------------------------------
    #   Verificar habitación disponible
    # ---------------------------------
    def habitacion_disponible(self, cur, num_hab):
        cur.execute("""
            SELECT estado_id
            FROM habitacion
            WHERE numero_habitacion = %s
        """, (num_hab,))
        hab = cur.fetchone()
        if not hab:
            return False, "La habitación no existe."
        if hab[0] != 1:
            return False, "La habitación no está disponible."
        return True, ""

    # ---------------------------------
    #   Actualizar estado habitación
    # ---------------------------------
    def ocupar_habitacion(self, cur, num_hab):
        cur.execute("UPDATE habitacion SET estado_id = 2 WHERE numero_habitacion=%s", (num_hab,))

    def liberar_habitacion(self, cur, num_hab):
        cur.execute("UPDATE habitacion SET estado_id = 1 WHERE numero_habitacion=%s", (num_hab,))

    # ---------------------------------
    #           Actualizar
    # ---------------------------------
    def actualizar(self):
        rid = self.reserva_id.text().strip()
        if not rid:
            QMessageBox.warning(self, "Error", "ID de reserva inválido.")
            return

        nuevo_hab = self.num_hab.text().strip()
        tiempo = self.tiempo_cancel.text().strip()
        salida = self.fecha_salida.date().toPython()
        llegada = self.fecha_llegada.date().toPython()

        if salida <= llegada:
            QMessageBox.warning(self, "Error", "La fecha de salida debe ser mayor a la llegada.")
            return

        conn = get_conn()
        cur = conn.cursor()

        try:
            # Si cambia de habitación
            if int(nuevo_hab) != self.old_habitacion:
                ok, msg = self.habitacion_disponible(cur, nuevo_hab)
                if not ok:
                    QMessageBox.warning(self, "Error", msg)
                    return

                # liberar la vieja
                self.liberar_habitacion(cur, self.old_habitacion)
                # ocupar la nueva
                self.ocupar_habitacion(cur, nuevo_hab)

            # actualizar reserva
            cur.execute("""
                UPDATE reserva SET
                    tiempo_max_cancelacion=%s,
                    fecha_salida=%s,
                    numero_habitacion=%s
                WHERE reserva_id=%s
            """, (tiempo, salida, nuevo_hab, rid))

            conn.commit()
            QMessageBox.information(self, "OK", "Reserva actualizada correctamente.")

        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Error", str(e))
        finally:
            conn.close()
