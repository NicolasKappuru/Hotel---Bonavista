# views/recepcion/reserva_list_view.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox
)
from PySide6.QtGui import QIntValidator
from db import get_conn

class ReservaListView(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main = main_window
        self.setWindowTitle("Listado de Reservas")
        self.resize(900, 600)

        # Campo para documento
        self.doc_input = QLineEdit()
        self.doc_input.setValidator(QIntValidator())
        self.doc_input.setPlaceholderText("Número de documento para buscar")
        self.btn_buscar = QPushButton("Buscar reservas")
        self.btn_buscar.clicked.connect(self.cargar)

        h_top = QHBoxLayout()
        h_top.addWidget(QLabel("Documento:"))
        h_top.addWidget(self.doc_input)
        h_top.addWidget(self.btn_buscar)

        # Tabla
        self.tabla = QTableWidget()

        layout = QVBoxLayout()
        layout.addLayout(h_top)
        layout.addWidget(self.tabla)
        self.setLayout(layout)

    def cargar(self):
        doc = self.doc_input.text().strip()
        if not doc:
            QMessageBox.warning(self, "Ingrese documento", "Digite un número de documento para buscar.")
            return

        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT 
                    r.reserva_id,
                    p.primer_nombre,
                    p.primer_apellido,
                    r.fecha_llegada,
                    r.fecha_salida,
                    COALESCE(SUM(s.costo_servicio), 0) AS costo_total
                FROM reserva r
                JOIN persona p 
                    ON p.tipo_documento = r.tipo_documento
                   AND p.numero_documento = r.numero_documento
                LEFT JOIN incluye i 
                    ON i.reserva_id = r.reserva_id
                LEFT JOIN servicio s 
                    ON s.servicio_id = i.servicio_id
                WHERE r.numero_documento = %s
                  AND CURRENT_DATE BETWEEN r.fecha_llegada AND r.fecha_salida
                GROUP BY 
                    r.reserva_id,
                    p.primer_nombre,
                    p.primer_apellido,
                    r.fecha_llegada,
                    r.fecha_salida
                ORDER BY r.reserva_id
            """, (doc,))
            rows = cur.fetchall()
            cols = [d[0] for d in cur.description]

            self.tabla.setColumnCount(len(cols))
            self.tabla.setHorizontalHeaderLabels(cols)
            self.tabla.setRowCount(len(rows))

            for i, row in enumerate(rows):
                for j, val in enumerate(row):
                    self.tabla.setItem(i, j, QTableWidgetItem(str(val)))
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        finally:
            conn.close()
