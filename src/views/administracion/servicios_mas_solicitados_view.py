from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox
)
from db import get_conn


class ServiciosMasSolicitadosView(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main = main_window
        self.setWindowTitle("Servicios más solicitados - Año 2025")
        self.resize(600, 400)

        # === Botón volver ===
        btn_back = QPushButton("Volver")
        btn_back.clicked.connect(self.main.ir_inicio_recepcion)

        h_top = QHBoxLayout()
        h_top.addStretch()
        h_top.addWidget(btn_back)

        # === Tabla ===
        self.tabla = QTableWidget()

        layout = QVBoxLayout()
        layout.addLayout(h_top)
        layout.addWidget(self.tabla)
        self.setLayout(layout)

        # carga automática
        self.cargar()


    def cargar(self):
        conn = get_conn()
        cur = conn.cursor()

        try:
            cur.execute("""
                SELECT
                    s.nombre_servicio,
                    COUNT(*) AS total_solicitudes
                FROM incluye i
                JOIN servicio s
                    ON s.servicio_id = i.servicio_id
                JOIN reserva r
                    ON r.reserva_id = i.reserva_id
                WHERE EXTRACT(YEAR FROM i.fecha_servicio) = 2025
                GROUP BY s.nombre_servicio
                ORDER BY total_solicitudes DESC;
            """)

            rows = cur.fetchall()
            cols = [d[0] for d in cur.description]

            self.tabla.setColumnCount(len(cols))
            self.tabla.setHorizontalHeaderLabels(cols)
            self.tabla.setRowCount(len(rows))

            for i, row in enumerate(rows):
                for j, val in enumerate(row):
                    self.tabla.setItem(i, j, QTableWidgetItem(str(val)))

            if not rows:
                QMessageBox.information(
                    self,
                    "Sin datos",
                    "No hay servicios registrados durante 2025."
                )

        except Exception as e:
            QMessageBox.critical(self, "Error en consulta", str(e))

        finally:
            conn.close()
