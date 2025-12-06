# views/administracion/empleado_delete_view.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QLabel,
    QPushButton, QMessageBox
)
from PySide6.QtGui import QIntValidator
from db import get_conn


class EmpleadoDeleteView(QWidget):

    def __init__(self, main_window=None):
        super().__init__(main_window)
        self.main = main_window
        self.setWindowTitle("Eliminar Empleado")
        self.resize(600, 300)

        # --- Campos solo lectura ---
        self.tipo_doc = QLineEdit()
        self.tipo_doc.setReadOnly(True)

        self.num_doc = QLineEdit()
        self.num_doc.setValidator(QIntValidator())

        self.nombre = QLineEdit()
        self.nombre.setReadOnly(True)

        self.apellidos = QLineEdit()
        self.apellidos.setReadOnly(True)

        self.cargo = QLineEdit()
        self.cargo.setReadOnly(True)

        self.area = QLineEdit()
        self.area.setReadOnly(True)

        # --- Botones ---
        self.btn_buscar = QPushButton("Buscar")
        self.btn_buscar.clicked.connect(self.buscar_empleado)

        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_eliminar.setEnabled(False)
        self.btn_eliminar.clicked.connect(self.eliminar_empleado)

        btn_volver = QPushButton("Volver")
        btn_volver.clicked.connect(self.main.ir_admin_home)

        # --- Layout consulta ---
        h_buscar = QHBoxLayout()
        h_buscar.addWidget(QLabel("Documento:"))
        h_buscar.addWidget(self.num_doc)
        h_buscar.addWidget(self.btn_buscar)

        # --- Formulario display ---
        form = QFormLayout()
        form.addRow("Tipo documento:", self.tipo_doc)
        form.addRow("Nombre:", self.nombre)
        form.addRow("Apellidos:", self.apellidos)
        form.addRow("Cargo:", self.cargo)
        form.addRow("Área:", self.area)

        # --- Layout botones ---
        h_botones = QHBoxLayout()
        h_botones.addWidget(self.btn_eliminar)
        h_botones.addWidget(btn_volver)

        # --- Layout general ---
        layout = QVBoxLayout()
        layout.addLayout(h_buscar)
        layout.addLayout(form)
        layout.addLayout(h_botones)
        layout.addStretch()

        self.setLayout(layout)

        # variables internas
        self.v_tipo_doc = None
        self.v_num_doc = None
        self.v_area_id = None

    # ======================================================
    # BUSCAR EMPLEADO
    # ======================================================
    def buscar_empleado(self):
        doc = self.num_doc.text().strip()
        if not doc:
            QMessageBox.warning(self, "Dato requerido", "Ingrese un número de documento.")
            return

        conn = get_conn()
        cur = conn.cursor()

        try:
            cur.execute("""
                SELECT e.tipo_documento, e.numero_documento,
                       p.primer_nombre, p.primer_apellido,
                       p.segundo_apellido, e.cargo, a.nombre_area
                FROM empleado e
                LEFT JOIN persona p
                    ON e.tipo_documento = p.tipo_documento
                   AND e.numero_documento = p.numero_documento
                LEFT JOIN area a
                    ON e.id_area = a.id_area
                WHERE e.numero_documento = %s
            """, (doc,))

            row = cur.fetchone()
            if not row:
                QMessageBox.information(self, "No existe", "No existe un empleado con ese documento.")
                return

            # Guardar valores internos para eliminar
            self.v_tipo_doc = row[0]
            self.v_num_doc = row[1]

            # Mostrar datos
            self.tipo_doc.setText(row[0])
            self.nombre.setText(row[2] or "")
            apellido_comp = f"{row[3] or ''} {row[4] or ''}".strip()
            self.apellidos.setText(apellido_comp)
            self.cargo.setText(row[5] or "")
            self.area.setText(row[6] or "")

            self.btn_eliminar.setEnabled(True)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        finally:
            conn.close()

    # ======================================================
    # ELIMINAR EMPLEADO
    # ======================================================
    def eliminar_empleado(self):
        if not self.v_tipo_doc or not self.v_num_doc:
            QMessageBox.warning(self, "No cargado", "Primero busque un empleado.")
            return

        tipo = self.v_tipo_doc
        numero = self.v_num_doc

        conn = get_conn()
        cur = conn.cursor()
        try:

            # 1) eliminar empleado
            cur.execute("""
                DELETE FROM empleado
                WHERE tipo_documento=%s AND numero_documento=%s
            """, (tipo, numero))

            # 2) verificar si persona sigue siendo cliente
            cur.execute("""
                SELECT 1 FROM cliente
                WHERE tipo_documento=%s AND numero_documento=%s
            """, (tipo, numero))
            es_cliente = cur.fetchone()

            # 3) verificar si persona sigue siendo huesped
            cur.execute("""
                SELECT 1 FROM huesped
                WHERE tipo_documento=%s AND numero_documento=%s
            """, (tipo, numero))
            es_huesped = cur.fetchone()

            # 4) si no es cliente ni huesped → eliminar persona
            if not es_cliente and not es_huesped:
                cur.execute("""
                    DELETE FROM persona
                    WHERE tipo_documento=%s AND numero_documento=%s
                """, (tipo, numero))

            conn.commit()
            QMessageBox.information(self, "OK", "Empleado eliminado correctamente.")

            # limpiar formulario
            self.tipo_doc.clear()
            self.nombre.clear()
            self.apellidos.clear()
            self.cargo.clear()
            self.area.clear()
            self.num_doc.clear()
            self.btn_eliminar.setEnabled(False)

        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Error", str(e))
        finally:
            conn.close()
