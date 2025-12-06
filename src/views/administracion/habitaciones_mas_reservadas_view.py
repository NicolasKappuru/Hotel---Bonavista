from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox
)
from db import get_conn


class HabitacionesMasReservadasView(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main = main_window
        self.setWindowTitle("Habitaciones más reservadas - Año 2025")
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

        # Cargar automáticamente
        self.cargar()


    def cargar(self):
        conn = get_conn()
        cur = conn.cursor()

        try:
            cur.execute("""
                SELECT
                    c.nombre_categoria,
                    COUNT(*) AS total_reservas
                FROM reserva r
                JOIN habitacion h
                    ON r.numero_habitacion = h.numero_habitacion
                JOIN categoria c
                    ON h.categoria_id = c.categoria_id
                WHERE EXTRACT(YEAR FROM r.fecha_llegada) = 2025
                GROUP BY c.nombre_categoria
                ORDER BY total_reservas DESC;
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
                    "No hay reservas registradas en 2025."
                )

        except Exception as e:
            QMessageBox.critical(self, "Error en consulta", str(e))

        finally:
            conn.close()
