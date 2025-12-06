# views/recepcion/cl iente_crud_view.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel,
    QPushButton, QCheckBox, QMessageBox, QFormLayout
)
from PySide6.QtWidgets import QDateEdit
from PySide6.QtCore import QDate
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QComboBox

from db import get_conn
from datetime import datetime

class ClienteInsertView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window


        titulo = QLabel("Gestión de Clientes / Huéspedes")
        titulo.setStyleSheet("font-size: 22px; font-weight: bold;")

        # Campos
        self.tipo_doc = QComboBox()
        self.tipo_doc.addItems(["CC", "TI"])        
        self.num_doc = QLineEdit()
        self.num_doc.setValidator(QIntValidator())
        self.p_nombre = QLineEdit()
        self.s_nombre = QLineEdit()
        self.p_apellido = QLineEdit()
        self.s_apellido = QLineEdit()
        self.correo = QLineEdit()
        self.carrera = QLineEdit()
        self.calle = QLineEdit()
        self.numero_casa = QLineEdit()
        self.complemento = QLineEdit()

        self.fecha_nacimiento = QDateEdit()
        self.fecha_nacimiento.setCalendarPopup(True)
        self.fecha_nacimiento.setDisplayFormat("yyyy-MM-dd")

        self.cb_cliente = QCheckBox("Cliente")
        self.cb_huesped = QCheckBox("Huésped")

        # Botones
        btn_insert = QPushButton("Insertar")
        btn_insert.clicked.connect(self.insertar)

 
        btn_back = QPushButton("Volver")
        btn_back.clicked.connect(self.main.ir_inicio_recepcion)
        
        # Formulario
        form = QFormLayout()
        form.addRow("Tipo documento:", self.tipo_doc)
        form.addRow("Número:", self.num_doc)
        form.addRow("Primer nombre:", self.p_nombre)
        form.addRow("Segundo nombre:", self.s_nombre)
        form.addRow("Primer apellido:", self.p_apellido)
        form.addRow("Segundo apellido:", self.s_apellido)
        form.addRow("Correo (si es cliente):", self.correo)
        form.addRow("Roles:", self.cb_cliente)
        form.addRow("Fecha nacimiento:", self.fecha_nacimiento)
        form.addRow("Carrera:", self.carrera)
        form.addRow("Calle:", self.calle)
        form.addRow("Número Casa:", self.numero_casa)
        form.addRow("Complemento:", self.complemento)

    
        form.addRow("", self.cb_huesped)

        botones = QHBoxLayout()
        botones.addWidget(btn_insert)
        botones.addWidget(btn_back)

        layout = QVBoxLayout()
        layout.addWidget(titulo)
        layout.addLayout(form)
        layout.addLayout(botones)
        layout.addStretch()

        self.setLayout(layout)

    # =============================
    #   INSERT
    # =============================
    def insertar(self):
        conn = get_conn()
        cur = conn.cursor()

        try:

            fecha_py = self.fecha_nacimiento.date().toPython()
            hoy = datetime.today().date()

            edad = (
                hoy.year 
                - fecha_py.year 
                - ((hoy.month, hoy.day) < (fecha_py.month, fecha_py.day))
            )

            if edad < 18 and self.cb_cliente.isChecked():
                QMessageBox.warning(self, "Restricción",
                                    "Un menor de edad NO puede ser cliente. Solo huésped.")
                return

            # Insert persona
            cur.execute("""
                INSERT INTO persona (
                    tipo_documento,
                    numero_documento,
                    primer_nombre,
                    segundo_nombre,
                    primer_apellido,
                    segundo_apellido,
                    fecha_nacimiento,
                    carrera,
                    calle,
                    numero,
                    complemento
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                self.tipo_doc.currentText() if hasattr(self.tipo_doc, "currentText") else self.tipo_doc.text(),
                self.num_doc.text(),
                self.p_nombre.text(),
                self.s_nombre.text(),
                self.p_apellido.text(),
                self.s_apellido.text(),
                self.fecha_nacimiento.date().toPython(),   # ← FECHA OK
                self.carrera.text() or None,
                self.calle.text() or None,
                self.numero_casa.text() or None,
                self.complemento.text() or None
            ))


            # Cliente
            if self.cb_cliente.isChecked():
                cur.execute("""
                INSERT INTO cliente (tipo_documento, numero_documento, correo_electronico)
                VALUES (%s,%s,%s)
                """, (
                    self.tipo_doc.currentText() if hasattr(self.tipo_doc, "currentText") else self.tipo_doc.text(),
                    self.num_doc.text(),
                    self.correo.text()
                ))

            # Huésped
            if self.cb_huesped.isChecked():
                cur.execute("""
                INSERT INTO huesped (tipo_documento, numero_documento)
                VALUES (%s,%s)
                """, (
                    self.tipo_doc.currentText() if hasattr(self.tipo_doc, "currentText") else self.tipo_doc.text(),
                    self.num_doc.text()
                ))

            conn.commit()
            QMessageBox.information(self, "OK", "Registro insertado correctamente.")

        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Error", str(e))

        finally:
            conn.close()
