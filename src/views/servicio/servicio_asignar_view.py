# views/servicio/servicio_asignar_view.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QMessageBox, QFormLayout, QComboBox, QDateEdit
)
from PySide6.QtGui import QIntValidator
from PySide6.QtCore import QDate
from db import get_conn


class ServicioAsignarView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window
        self.setWindowTitle("Asignar Servicio a Reserva")

        # -------------------------------
        # CAMPOS
        # -------------------------------

        self.reserva_id = QLineEdit()
        self.reserva_id.setValidator(QIntValidator())

        self.servicio_combo = QComboBox()

        self.fecha_serv = QDateEdit()
        self.fecha_serv.setCalendarPopup(True)
        self.fecha_serv.setDisplayFormat("yyyy-MM-dd")

        self.fecha_llegada = None
        self.fecha_salida = None

        # -------------------------------
        # BOTONES
        # -------------------------------
        btn_buscar = QPushButton("Verificar Reserva")
        btn_buscar.clicked.connect(self.verificar_reserva)

        btn_asignar = QPushButton("Asignar Servicio")
        btn_asignar.clicked.connect(self.asignar)
        self.btn_asignar = btn_asignar
        self.btn_asignar.setEnabled(False)

        btn_back = QPushButton("Volver")
        btn_back.clicked.connect(self.main.ir_inicio_servicio)

        # -------------------------------
        # FORM
        # -------------------------------
        form = QFormLayout()
        form.addRow("ID Reserva:", self.reserva_id)
        form.addRow("Servicio:", self.servicio_combo)
        form.addRow("Fecha del Servicio:", self.fecha_serv)

        botones = QHBoxLayout()
        botones.addWidget(btn_buscar)
        botones.addWidget(btn_asignar)
        botones.addWidget(btn_back)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Asignar Servicio a una Reserva"))
        layout.addLayout(form)
        layout.addLayout(botones)
        layout.addStretch()

        self.setLayout(layout)

        self.cargar_servicios()

    # --------------------------------------------------------------
    # CARGAR SERVICIOS EN EL COMBOBOX
    # --------------------------------------------------------------
    def cargar_servicios(self):
        conn = get_conn()
        cur = conn.cursor()

        try:
            cur.execute("SELECT servicio_id, nombre_servicio FROM servicio ORDER BY servicio_id")
            servicios = cur.fetchall()

            self.servicio_combo.clear()
            for sid, nombre in servicios:
                self.servicio_combo.addItem(nombre, sid)

        except Exception as e:
            print("Error cargando servicios:", e)
        finally:
            conn.close()

    # --------------------------------------------------------------
    # VERIFICAR RESERVA Y OBTENER FECHAS
    # --------------------------------------------------------------
    def verificar_reserva(self):
        rid = self.reserva_id.text().strip()
        if not rid:
            QMessageBox.warning(self, "Error", "Ingrese un ID de reserva.")
            return

        conn = get_conn()
        cur = conn.cursor()

        try:
            cur.execute("""
                SELECT fecha_llegada, fecha_salida
                FROM reserva
                WHERE reserva_id = %s
            """, (rid,))
            r = cur.fetchone()

            if not r:
                QMessageBox.warning(self, "Error", "La reserva NO existe.")
                return

            self.fecha_llegada = r[0]
            self.fecha_salida = r[1]

            # establecer fecha por defecto = llegada
            self.fecha_serv.setDate(QDate(self.fecha_llegada.year, self.fecha_llegada.month, self.fecha_llegada.day))

            self.btn_asignar.setEnabled(True)
            QMessageBox.information(self, "OK", "Reserva encontrada. Puede asignar servicios.")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        finally:
            conn.close()

    # --------------------------------------------------------------
    # ASIGNAR SERVICIO A RESERVA
    # --------------------------------------------------------------
    def asignar(self):
        rid = self.reserva_id.text().strip()
        sid = self.servicio_combo.currentData()
        fecha = self.fecha_serv.date().toPython()

        # Validar fechas dentro del rango
        if fecha < self.fecha_llegada or fecha > self.fecha_salida:
            QMessageBox.warning(
                self, "Fecha inválida",
                "La fecha debe estar entre la fecha de llegada y la fecha de salida de la reserva."
            )
            return

        conn = get_conn()
        cur = conn.cursor()

        try:
            # Insertar en INCLUYE
            cur.execute("""
                INSERT INTO incluye (fecha_servicio, reserva_id, servicio_id)
                VALUES (%s, %s, %s)
            """, (fecha, rid, sid))

            conn.commit()
            QMessageBox.information(self, "OK", "Servicio asignado correctamente.")

        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Error", str(e))
        finally:
            conn.close()
