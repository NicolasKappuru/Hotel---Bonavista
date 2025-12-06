from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)
from PySide6.QtGui import QIntValidator
from db import get_conn


class EmpleadoConsultarView(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main = main_window
        self.setWindowTitle("Consulta Empleado")
        self.resize(800, 400)

        # === Campo documento ===
        self.doc_input = QLineEdit()
        self.doc_input.setValidator(QIntValidator())
        self.doc_input.setPlaceholderText("Número de documento")

        btn_buscar = QPushButton("Consultar")
        btn_buscar.clicked.connect(self.cargar)

        btn_back = QPushButton("Volver")
        btn_back.clicked.connect(self.main.ir_inicio_recepcion)

        h_top = QHBoxLayout()
        h_top.addWidget(QLabel("Documento:"))
        h_top.addWidget(self.doc_input)
        h_top.addWidget(btn_buscar)
        h_top.addWidget(btn_back)

        # === Tabla ===
        self.tabla = QTableWidget()

        layout = QVBoxLayout()
        layout.addLayout(h_top)
        layout.addWidget(self.tabla)
        self.setLayout(layout)


    def cargar(self):
        doc = self.doc_input.text().strip()
        if not doc:
            QMessageBox.warning(self, "Campo requerido", "Ingrese un número de documento.")
            return

        conn = get_conn()
        cur = conn.cursor()

        try:
            cur.execute("""
                SELECT 
                    e.tipo_documento,
                    e.numero_documento,
                    p.primer_nombre,
                    p.segundo_nombre,
                    p.primer_apellido,
                    p.segundo_apellido,
                    e.cargo,
                    a.nombre_area
                FROM empleado e
                JOIN persona p
                    ON e.tipo_documento = p.tipo_documento
                   AND e.numero_documento = p.numero_documento
                JOIN area a
                    ON a.id_area = e.id_area
                WHERE e.numero_documento = %s;
            """, (doc,))

            rows = cur.fetchall()
            cols = [d[0] for d in cur.description]

            # === Configurar tabla ===
            self.tabla.setColumnCount(len(cols))
            self.tabla.setHorizontalHeaderLabels(cols)
            self.tabla.setRowCount(len(rows))

            for i, row in enumerate(rows):
                for j, val in enumerate(row):
                    self.tabla.setItem(i, j, QTableWidgetItem(str(val)))

            if not rows:
                QMessageBox.information(self, "Sin resultados",
                    "No se encontró empleado para ese documento.")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

        finally:
            conn.close()
