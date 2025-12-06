# views/administracion/servicio_update_view.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QMessageBox
)
from PySide6.QtGui import QDoubleValidator
from db import get_conn


class ServiciosActualizarView(QWidget):
    def __init__(self, main_window=None):
        super().__init__(main_window)
        self.main = main_window
        self.setWindowTitle("Actualizar Servicio")
        self.resize(600, 400)

        # -------------------------------------------------
        #   SELECTOR DE SERVICIO
        # -------------------------------------------------
        self.selector_servicio = QComboBox()
        self.selector_servicio.currentIndexChanged.connect(self.cargar_servicio)

        # -------------------------------------------------
        #   CAMPOS (algunos readonly)
        # -------------------------------------------------
        self.servicio_id = QLineEdit()
        self.servicio_id.setReadOnly(True)

        self.nombre_servicio = QLineEdit()
        self.nombre_servicio.setReadOnly(True)

        self.descripcion = QLineEdit()

        self.costo = QLineEdit()
        self.costo.setValidator(QDoubleValidator(0, 999999, 2))

        # -------------------------------------------------
        #   BOTONES
        # -------------------------------------------------
        btn_actualizar = QPushButton("Actualizar")
        btn_actualizar.clicked.connect(self.actualizar_servicio)

        btn_volver = QPushButton("Volver")
        btn_volver.clicked.connect(self.main.ir_admin_home)

        # -------------------------------------------------
        #   FORMULARIO
        # -------------------------------------------------
        form = QFormLayout()
        form.addRow("Seleccionar servicio:", self.selector_servicio)
        form.addRow("ID:", self.servicio_id)
        form.addRow("Nombre:", self.nombre_servicio)
        form.addRow("Descripción:", self.descripcion)
        form.addRow("Costo:", self.costo)

        h_botones = QHBoxLayout()
        h_botones.addWidget(btn_actualizar)
        h_botones.addWidget(btn_volver)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addLayout(h_botones)
        layout.addStretch()
        self.setLayout(layout)

        # Cargar los servicios al iniciar
        self.cargar_lista_servicios()

    # ======================================================
    #   CARGAR OPCIONES DE SERVICIO
    # ======================================================
    def cargar_lista_servicios(self):
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute("SELECT servicio_id, nombre_servicio FROM servicio ORDER BY servicio_id")
            servicios = cur.fetchall()

            self.selector_servicio.clear()
            for sid, nombre in servicios:
                self.selector_servicio.addItem(f"{sid} - {nombre}", sid)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        finally:
            conn.close()

    # ======================================================
    #   CARGAR DATOS DEL SERVICIO SELECCIONADO
    # ======================================================
    def cargar_servicio(self):
        sid = self.selector_servicio.currentData()
        if sid is None:
            return

        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT servicio_id, nombre_servicio, descripcion, costo_servicio
                FROM servicio
                WHERE servicio_id = %s
            """, (sid,))
            row = cur.fetchone()
            if not row:
                return

            # Cargar valores
            self.servicio_id.setText(str(row[0]))
            self.nombre_servicio.setText(row[1])
            self.descripcion.setText(row[2])
            self.costo.setText(str(row[3]))

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        finally:
            conn.close()

    # ======================================================
    #   ACTUALIZAR SERVICIO
    # ======================================================
    def actualizar_servicio(self):
        sid = self.servicio_id.text().strip()
        descripcion = self.descripcion.text().strip()
        costo = self.costo.text().strip()

        if not sid:
            QMessageBox.warning(self, "Dato faltante", "Seleccione un servicio primero.")
            return

        if not descripcion:
            QMessageBox.warning(self, "Dato faltante", "La descripción no puede estar vacía.")
            return

        if not costo:
            QMessageBox.warning(self, "Dato faltante", "El costo no puede estar vacío.")
            return

        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE servicio
                SET descripcion=%s,
                    costo_servicio=%s
                WHERE servicio_id=%s
            """, (descripcion, costo, sid))

            conn.commit()
            QMessageBox.information(self, "OK", "Servicio actualizado correctamente.")

        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Error", str(e))
        finally:
            conn.close()
