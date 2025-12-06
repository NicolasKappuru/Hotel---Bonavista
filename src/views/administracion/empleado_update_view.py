# views/administracion/empleado_update_view.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QLabel,
    QPushButton, QMessageBox, QComboBox, QDateEdit
)
from PySide6.QtGui import QIntValidator
from PySide6.QtCore import QDate
from datetime import datetime
from db import get_conn


class EmpleadoUpdateView(QWidget):

    def __init__(self, main_window=None):
        super().__init__(main_window)
        self.main = main_window
        self.setWindowTitle("Actualizar Empleado")
        self.resize(800, 500)

        # --- Campos persona ---
        self.tipo_doc = QComboBox()
        self.tipo_doc.addItems(["CC"])
        self.tipo_doc.setEnabled(False)

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
        self.complemento = QLineEdit()

        # --- Campos empleado ---
        self.cargo_combo = QComboBox()
        self.cargo_combo.addItems([
            "Administrador",
            "Recepcionista",
            "Personal Servicio",
            "Aseador",
            "Tecnico"
        ])

        self.area_combo = QComboBox()

        # --- Barra de consulta ---
        self.input_buscar = QLineEdit()
        self.input_buscar.setValidator(QIntValidator())
        self.input_buscar.setPlaceholderText("Número de documento para buscar empleado")

        self.btn_buscar = QPushButton("Buscar")
        self.btn_buscar.clicked.connect(self.buscar_empleado)

        h_buscar = QHBoxLayout()
        h_buscar.addWidget(QLabel("Consultar:"))
        h_buscar.addWidget(self.input_buscar)
        h_buscar.addWidget(self.btn_buscar)

        # --- Botones ---
        self.btn_actualizar = QPushButton("Actualizar")
        self.btn_actualizar.setEnabled(False)
        self.btn_actualizar.clicked.connect(self.actualizar_empleado)

        btn_volver = QPushButton("Volver")
        btn_volver.clicked.connect(self.main.ir_admin_home)

        h_botones = QHBoxLayout()
        h_botones.addWidget(self.btn_actualizar)
        h_botones.addWidget(btn_volver)

        # --- Formulario ---
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
        form.addRow("Número casa:", self.numero_casa)
        form.addRow("Complemento:", self.complemento)
        form.addRow("Cargo:", self.cargo_combo)
        form.addRow("Área:", self.area_combo)

        # --- Layout principal ---
        layout = QVBoxLayout()
        layout.addLayout(h_buscar)
        layout.addLayout(form)
        layout.addLayout(h_botones)
        layout.addStretch()
        self.setLayout(layout)

    # ----------------------------------------------------
    # Buscar empleado por numero_documento y cargar persona
    # ----------------------------------------------------
    def buscar_empleado(self):
        doc = self.input_buscar.text().strip()
        if not doc:
            QMessageBox.warning(self, "Dato requerido", "Ingrese un número de documento.")
            return

        conn = get_conn()
        cur = conn.cursor()
        try:
            # Traer datos de empleado + persona si existen
            cur.execute("""
                SELECT e.tipo_documento, e.numero_documento,
                       p.primer_nombre, p.segundo_nombre,
                       p.primer_apellido, p.segundo_apellido,
                       p.fecha_nacimiento, p.carrera, p.calle, p.numero, p.complemento,
                       e.cargo, e.id_area
                FROM empleado e
                LEFT JOIN persona p
                  ON e.tipo_documento = p.tipo_documento
                 AND e.numero_documento = p.numero_documento
                WHERE e.numero_documento = %s
            """, (doc,))
            row = cur.fetchone()
            if not row:
                QMessageBox.information(self, "No encontrado", "No existe empleado con ese documento.")
                return

            # Cargar persona
            tipo, numero = row[0], row[1]
            self.tipo_doc.setCurrentText(tipo)
            self.num_doc.setText(numero)

            self.p_nombre.setText(row[2] or "")
            self.s_nombre.setText(row[3] or "")
            self.p_apellido.setText(row[4] or "")
            self.s_apellido.setText(row[5] or "")

            if row[6]:
                if isinstance(row[6], str):
                    self.fecha_nacimiento.setDate(QDate.fromString(row[6], "yyyy-MM-dd"))
                else:
                    self.fecha_nacimiento.setDate(row[6])
            else:
                self.fecha_nacimiento.setDate(QDate.currentDate())

            self.carrera.setText(row[7] or "")
            self.calle.setText(row[8] or "")
            self.numero_casa.setText(str(row[9] or ""))
            self.complemento.setText(row[10] or "")

            # Cargar empleado
            cargo_actual = row[11]
            id_area_actual = row[12]

            # Cargar áreas y seleccionar la actual
            self.cargar_areas(desired_id=id_area_actual)

            # Seleccionar cargo en combo (si existe)
            idx = self.cargo_combo.findText(cargo_actual) if cargo_actual else -1
            if idx >= 0:
                self.cargo_combo.setCurrentIndex(idx)

            self.btn_actualizar.setEnabled(True)
            QMessageBox.information(self, "Cargado", "Empleado cargado. Modifique y presione Actualizar.")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        finally:
            conn.close()

    # ----------------------------------------------------
    # Cargar lista de áreas desde BD y seleccionar el área actual
    # ----------------------------------------------------
    def cargar_areas(self, desired_id=None):
        self.area_combo.clear()
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute("SELECT id_area, nombre_area FROM area ORDER BY nombre_area")
            rows = cur.fetchall()
            for id_area, nombre in rows:
                self.area_combo.addItem(nombre, id_area)

            if desired_id is not None:
                idx = self.area_combo.findData(desired_id)
                if idx >= 0:
                    self.area_combo.setCurrentIndex(idx)

        except Exception as e:
            QMessageBox.critical(self, "Error cargando áreas", str(e))
        finally:
            conn.close()

    # ----------------------------------------------------
    # Actualizar empleado (persona + empleado)
    # ----------------------------------------------------
    def actualizar_empleado(self):
        # Validaciones mínimas
        if not self.num_doc.text().isdigit():
            QMessageBox.warning(self, "Dato inválido", "El número de documento solo puede tener dígitos.")
            return

        # Edad mínima 18
        fecha_py = self.fecha_nacimiento.date().toPython()
        hoy = datetime.today().date()
        edad = hoy.year - fecha_py.year - ((hoy.month, hoy.day) < (fecha_py.month, fecha_py.day))
        if edad < 18:
            QMessageBox.warning(self, "Restricción", "Un empleado NO puede ser menor de 18 años.")
            return

        tipo = self.tipo_doc.currentText()
        numero = self.num_doc.text().strip()
        cargo = self.cargo_combo.currentText()
        id_area = self.area_combo.currentData()

        conn = get_conn()
        cur = conn.cursor()
        try:
            # actualizar persona (si existe)
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

            # actualizar empleado
            cur.execute("""
                UPDATE empleado SET
                    cargo=%s,
                    id_area=%s
                WHERE tipo_documento=%s AND numero_documento=%s
            """, (cargo, id_area, tipo, numero))

            conn.commit()
            QMessageBox.information(self, "OK", "Empleado actualizado correctamente.")
            self.btn_actualizar.setEnabled(False)
        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Error", str(e))
        finally:
            conn.close()
