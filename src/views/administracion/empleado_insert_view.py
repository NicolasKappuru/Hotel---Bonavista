# views/administracion/empleado_insertar_view.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel,
    QPushButton, QMessageBox, QFormLayout, QComboBox, QDateEdit
)
from PySide6.QtGui import QIntValidator
from PySide6.QtCore import QDate
from datetime import datetime
from db import get_conn


class EmpleadoInsertView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window

        titulo = QLabel("Insertar Empleado")
        titulo.setStyleSheet("font-size: 22px; font-weight: bold;")

        # Campos Persona
        self.tipo_doc = QComboBox()
        self.tipo_doc.addItems(["CC"])

        self.num_doc = QLineEdit()
        self.num_doc.setValidator(QIntValidator())

        self.p_nombre = QLineEdit()
        self.s_nombre = QLineEdit()
        self.p_apellido = QLineEdit()
        self.s_apellido = QLineEdit()

        self.fecha_nacimiento = QDateEdit()
        self.fecha_nacimiento.setCalendarPopup(True)
        self.fecha_nacimiento.setDisplayFormat("yyyy-MM-dd")

        self.carrera = QLineEdit()
        self.calle = QLineEdit()
        self.numero_casa = QLineEdit()
        self.complemento = QLineEdit()

        # Select Áreas (desde BD)
        self.area_combo = QComboBox()

        # Select Cargos (fijos)
        self.cargo_combo = QComboBox()
        self.cargo_combo.addItems([
            "Administrador",
            "Recepcionista",
            "Personal Servicio",
            "Aseador",
            "Tecnico"
        ])

        # Botones
        btn_insert = QPushButton("Insertar")
        btn_insert.clicked.connect(self.insertar)

        btn_back = QPushButton("Volver")
        btn_back.clicked.connect(self.main.ir_admin_home)

        # Cargar áreas
        self.cargar_areas()

        # Formulario
        form = QFormLayout()
        form.addRow("Tipo Documento:", self.tipo_doc)
        form.addRow("Número Documento:", self.num_doc)
        form.addRow("Primer Nombre:", self.p_nombre)
        form.addRow("Segundo Nombre:", self.s_nombre)
        form.addRow("Primer Apellido:", self.p_apellido)
        form.addRow("Segundo Apellido:", self.s_apellido)
        form.addRow("Fecha Nacimiento:", self.fecha_nacimiento)
        form.addRow("Carrera:", self.carrera)
        form.addRow("Calle:", self.calle)
        form.addRow("Número Casa:", self.numero_casa)
        form.addRow("Complemento:", self.complemento)

        form.addRow("Área:", self.area_combo)
        form.addRow("Cargo:", self.cargo_combo)

        hbotones = QHBoxLayout()
        hbotones.addWidget(btn_insert)
        hbotones.addWidget(btn_back)

        layout = QVBoxLayout()
        layout.addWidget(titulo)
        layout.addLayout(form)
        layout.addLayout(hbotones)
        layout.addStretch()

        self.setLayout(layout)

    def cargar_areas(self):
        conn = get_conn()
        cur = conn.cursor()
        try:
            # Columnas correctas según tu tabla AREA
            cur.execute("SELECT id_area, nombre_area FROM area ORDER BY id_area")
            areas = cur.fetchall()

            self.area_combo.clear()

            for aid, nombre in areas:
                self.area_combo.addItem(nombre, aid)

        except Exception as e:
            print("Error cargando áreas:", e)
            self.area_combo.clear()
            self.area_combo.addItem("Error al cargar áreas", None)

        finally:
            conn.close()

    # =============================
    #         INSERTAR
    # =============================
    def insertar(self):
        conn = get_conn()
        cur = conn.cursor()

        try:
            # Validación edad
            fecha_nac = self.fecha_nacimiento.date().toPython()
            hoy = datetime.today().date()

            edad = (
                hoy.year
                - fecha_nac.year
                - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
            )

            if edad < 18:
                QMessageBox.warning(self, "Restricción",
                                    "Un empleado NO puede ser menor de 18 años.")
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
                self.tipo_doc.currentText(),
                self.num_doc.text(),
                self.p_nombre.text(),
                self.s_nombre.text(),
                self.p_apellido.text(),
                self.s_apellido.text(),
                fecha_nac,
                self.carrera.text() or None,
                self.calle.text() or None,
                self.numero_casa.text() or None,
                self.complemento.text() or None
            ))

            cur.execute("""
                INSERT INTO empleado (
                    tipo_documento,
                    numero_documento,
                    cargo,
                    id_area
                ) VALUES (%s, %s, %s, %s)
            """, (
                self.tipo_doc.currentText(),
                self.num_doc.text(),
                self.cargo_combo.currentText(),      
                self.area_combo.currentData()          
            ))

            conn.commit()
            QMessageBox.information(self, "OK", "Empleado insertado correctamente.")

        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Error", str(e))

        finally:
            conn.close()
