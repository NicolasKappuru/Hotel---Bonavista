# views/recepcion/cliente_update_view.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QLabel,
    QPushButton, QCheckBox, QMessageBox, QComboBox, QDateEdit
)
from PySide6.QtGui import QIntValidator
from PySide6.QtCore import QDate
from datetime import datetime
from db import get_conn

class ClienteUpdateView(QWidget):
    """
    Vista exclusiva para BUSCAR y ACTUALIZAR una persona (persona + cliente + huesped).
    - Buscar por número de documento
    - Cargar campos en el formulario
    - Editar y pulsar Actualizar
    - Tipo_documento y numero_documento se bloquean (no pueden cambiar)
    """
    def __init__(self, main_window=None):
        super().__init__(main_window)
        self.main = main_window
        self.setWindowTitle("Actualizar Cliente / Huésped")
        self.resize(900, 600)

        # --- Form fields (mismos que insertar) ---
        self.tipo_doc = QComboBox()
        self.tipo_doc.addItems(["CC", "TI"])
        self.tipo_doc.setEnabled(False)  # se desbloquea solo cuando se carga un registro

        self.num_doc = QLineEdit()
        self.num_doc.setValidator(QIntValidator())
        self.num_doc.setEnabled(False)

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
        self.numero_casa.setValidator(QIntValidator())
        self.complemento = QLineEdit()

        self.cb_cliente = QCheckBox("Cliente")
        self.cb_huesped = QCheckBox("Huésped")
        self.correo = QLineEdit()

        # Botones
        self.btn_buscar = QPushButton("Buscar")
        self.btn_buscar.clicked.connect(self.buscar_persona)

        self.btn_actualizar = QPushButton("Actualizar")
        self.btn_actualizar.clicked.connect(self.actualizar)
        self.btn_actualizar.setEnabled(False)  # solo activo después de cargar persona

        self.btn_volver = QPushButton("Volver")
        if self.main:
            self.btn_volver.clicked.connect(self.main.ir_inicio_recepcion)
        else:
            self.btn_volver.clicked.connect(self.close)

        # Layouts
        form = QFormLayout()
        form.addRow("Tipo documento:", self.tipo_doc)
        form.addRow("Número documento:", self.num_doc)
        form.addRow("Primer nombre:", self.p_nombre)
        form.addRow("Segundo nombre:", self.s_nombre)
        form.addRow("Primer apellido:", self.p_apellido)
        form.addRow("Segundo apellido:", self.s_apellido)
        form.addRow("Fecha nacimiento:", self.fecha_nacimiento)
        form.addRow("Carrera:", self.carrera)
        form.addRow("Calle:", self.calle)
        form.addRow("Número:", self.numero_casa)
        form.addRow("Complemento:", self.complemento)
        form.addRow(self.cb_cliente, self.correo)
        form.addRow(self.cb_huesped)

        h_buttons = QHBoxLayout()
        h_buttons.addWidget(self.btn_actualizar)
        h_buttons.addWidget(self.btn_volver)

        # Consulta rápida abajo
        h_consulta = QHBoxLayout()
        self.consulta_doc = QLineEdit()
        self.consulta_doc.setPlaceholderText("Número de documento para buscar")
        self.consulta_doc.setValidator(QIntValidator())
        h_consulta.addWidget(QLabel("Consultar por documento:"))
        h_consulta.addWidget(self.consulta_doc)
        h_consulta.addWidget(self.btn_buscar)

        main_layout = QVBoxLayout()
        main_layout.addLayout(h_consulta)
        main_layout.addLayout(form)
        main_layout.addLayout(h_buttons)
        main_layout.addStretch()
        self.setLayout(main_layout)

    # -----------------------
    # Buscar y cargar persona
    # -----------------------
    def buscar_persona(self):
        doc = self.consulta_doc.text().strip()
        if not doc:
            QMessageBox.warning(self, "Ingrese documento", "Digite un número de documento para buscar.")
            return
        if not doc.isdigit():
            QMessageBox.warning(self, "Dato inválido", "El documento debe contener solo dígitos.")
            return

        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT tipo_documento, numero_documento,
                       primer_nombre, segundo_nombre,
                       primer_apellido, segundo_apellido,
                       fecha_nacimiento, carrera, calle, numero, complemento
                FROM persona
                WHERE numero_documento = %s
            """, (doc,))
            persona = cur.fetchone()
            if not persona:
                QMessageBox.information(self, "No encontrado", "No existe persona con ese número.")
                return

            # cargar datos en formulario
            tipo, numero = persona[0], persona[1]
            # tipo puede no estar en combo, intentamos setear
            if tipo not in [self.tipo_doc.itemText(i) for i in range(self.tipo_doc.count())]:
                self.tipo_doc.addItem(tipo)
            self.tipo_doc.setCurrentText(tipo)
            self.tipo_doc.setEnabled(False)

            self.num_doc.setText(numero)
            self.num_doc.setEnabled(False)

            self.p_nombre.setText(persona[2] or "")
            self.s_nombre.setText(persona[3] or "")
            self.p_apellido.setText(persona[4] or "")
            self.s_apellido.setText(persona[5] or "")

            # fecha_nacimiento puede venir como date
            if persona[6]:
                if isinstance(persona[6], str):
                    # intentar parsear
                    self.fecha_nacimiento.setDate(QDate.fromString(persona[6], "yyyy-MM-dd"))
                else:
                    self.fecha_nacimiento.setDate(persona[6])
            else:
                self.fecha_nacimiento.setDate(QDate.currentDate())

            self.carrera.setText(persona[7] or "")
            self.calle.setText(persona[8] or "")
            self.numero_casa.setText(str(persona[9] or ""))
            self.complemento.setText(persona[10] or "")

            # cliente?
            cur.execute("""
                SELECT correo_electronico FROM cliente
                WHERE tipo_documento=%s AND numero_documento=%s
            """, (tipo, numero))
            cli = cur.fetchone()
            if cli:
                self.cb_cliente.setChecked(True)
                self.correo.setText(cli[0] or "")
            else:
                self.cb_cliente.setChecked(False)
                self.correo.setText("")

            # huesped?
            cur.execute("""
                SELECT 1 FROM huesped
                WHERE tipo_documento=%s AND numero_documento=%s
            """, (tipo, numero))
            hues = cur.fetchone()
            self.cb_huesped.setChecked(bool(hues))

            # permitir actualizar ahora
            self.btn_actualizar.setEnabled(True)
            QMessageBox.information(self, "Cargado", "Datos cargados. Modifica y presiona Actualizar.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        finally:
            conn.close()

    # -----------------------
    # Actualizar
    # -----------------------
    def actualizar(self):
        # validaciones
        if not self.num_doc.text().isdigit():
            QMessageBox.warning(self, "Dato inválido", "El número de documento solo puede tener dígitos.")
            return

        fecha_py = self.fecha_nacimiento.date().toPython()
        hoy = datetime.today().date()
        edad = hoy.year - fecha_py.year - ((hoy.month, hoy.day) < (fecha_py.month, fecha_py.day))

        if edad < 18 and self.cb_cliente.isChecked():
            QMessageBox.warning(self, "Restricción", "Un menor de edad NO puede ser cliente.")
            return

        tipo = self.tipo_doc.currentText()
        numero = self.num_doc.text()

        conn = get_conn()
        cur = conn.cursor()
        try:
            # actualizar persona
            cur.execute("""
                UPDATE persona SET
                    primer_nombre=%s, segundo_nombre=%s,
                    primer_apellido=%s, segundo_apellido=%s,
                    fecha_nacimiento=%s, carrera=%s, calle=%s, numero=%s, complemento=%s
                WHERE tipo_documento=%s AND numero_documento=%s
            """, (
                self.p_nombre.text() or None,
                self.s_nombre.text() or None,
                self.p_apellido.text() or None,
                self.s_apellido.text() or None,
                fecha_py,
                self.carrera.text() or None,
                self.calle.text() or None,
                self.numero_casa.text() or None,
                self.complemento.text() or None,
                tipo,
                numero
            ))

            # manejar cliente: update o insert si no existia
            if self.cb_cliente.isChecked():
                cur.execute("""
                    UPDATE cliente SET correo_electronico=%s
                    WHERE tipo_documento=%s AND numero_documento=%s
                """, (self.correo.text() or None, tipo, numero))
                if cur.rowcount == 0:
                    cur.execute("""
                        INSERT INTO cliente (tipo_documento, numero_documento, correo_electronico)
                        VALUES (%s, %s, %s)
                    """, (tipo, numero, self.correo.text() or None))
            else:
                # no eliminamos registro cliente aunque se desmarque
                pass

            # manejar huesped: si está marcado e no existe → insertar; si no marcado → no borramos
            if self.cb_huesped.isChecked():
                cur.execute("""
                    INSERT INTO huesped (tipo_documento, numero_documento)
                    SELECT %s, %s
                    WHERE NOT EXISTS (
                        SELECT 1 FROM huesped WHERE tipo_documento=%s AND numero_documento=%s
                    )
                """, (tipo, numero, tipo, numero))

            conn.commit()
            QMessageBox.information(self, "OK", "Datos actualizados correctamente.")
        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Error", str(e))
        finally:
            conn.close()
