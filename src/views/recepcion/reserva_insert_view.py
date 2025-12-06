from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel,
    QPushButton, QMessageBox, QFormLayout, QComboBox, QDateEdit
)
from PySide6.QtCore import QDate
from PySide6.QtGui import QIntValidator

from db import get_conn
from datetime import date


class ReservaInsertView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window

        titulo = QLabel("Gestión de Reservas")
        titulo.setStyleSheet("font-size: 22px; font-weight: bold;")

        # Campos
        self.tipo_doc = QComboBox()
        self.tipo_doc.addItems(["CC", "TI"])

        self.num_doc = QLineEdit()
        self.num_doc.setValidator(QIntValidator())

        self.num_habitacion = QLineEdit()
        self.num_habitacion.setValidator(QIntValidator())

        self.tiempo_cancel = QLineEdit()
        self.tiempo_cancel.setValidator(QIntValidator())
        self.tiempo_cancel.setText("48")  # por defecto

        # Fecha llegada automática = HOY
        self.fecha_llegada = QDateEdit()
        self.fecha_llegada.setDate(QDate.currentDate())
        self.fecha_llegada.setReadOnly(True)
        self.fecha_llegada.setCalendarPopup(True)
        self.fecha_llegada.setDisplayFormat("yyyy-MM-dd")

        # Fecha salida editable pero debe ser > llegada
        self.fecha_salida = QDateEdit()
        self.fecha_salida.setCalendarPopup(True)
        self.fecha_salida.setDisplayFormat("yyyy-MM-dd")
        self.fecha_salida.setDate(QDate.currentDate().addDays(1))

        # Botones
        btn_insert = QPushButton("Crear Reserva")
        btn_insert.clicked.connect(self.insertar)

        btn_back = QPushButton("Volver")
        btn_back.clicked.connect(self.main.ir_inicio_recepcion)

        # Formulario
        form = QFormLayout()
        form.addRow("Tipo documento:", self.tipo_doc)
        form.addRow("Número documento:", self.num_doc)
        form.addRow("Número habitación:", self.num_habitacion)
        form.addRow("Tiempo máx. cancelación (horas):", self.tiempo_cancel)
        form.addRow("Fecha llegada:", self.fecha_llegada)
        form.addRow("Fecha salida:", self.fecha_salida)

        botones = QHBoxLayout()
        botones.addWidget(btn_insert)
        botones.addWidget(btn_back)

        layout = QVBoxLayout()
        layout.addWidget(titulo)
        layout.addLayout(form)
        layout.addLayout(botones)
        layout.addStretch()

        self.setLayout(layout)

    # ==========================================================
    #                    INSERTAR RESERVA
    # ==========================================================
    def insertar(self):
        conn = get_conn()
        cur = conn.cursor()

        self.sincronizar_secuencia_reserva(cur)

        try:
            tipo_doc = self.tipo_doc.currentText()
            num_doc = self.num_doc.text()
            num_hab = self.num_habitacion.text()
            tiempo_max = int(self.tiempo_cancel.text())

            fecha_lleg = self.fecha_llegada.date().toPython()
            fecha_sal = self.fecha_salida.date().toPython()

            # -------------------------------------------
            # Validar fechas
            # -------------------------------------------
            if fecha_sal <= fecha_lleg:
                QMessageBox.warning(
                    self, "Fecha inválida",
                    "La fecha de salida debe ser mayor a la de llegada."
                )
                return

            # -------------------------------------------
            # Validar persona existente
            # -------------------------------------------
            cur.execute("""
                SELECT 1 FROM persona
                WHERE tipo_documento=%s AND numero_documento=%s
            """, (tipo_doc, num_doc))

            if cur.fetchone() is None:
                QMessageBox.warning(
                    self, "Error",
                    "La persona NO existe. Primero debe registrarla."
                )
                return

            # -------------------------------------------
            # Validar habitación existente y disponible
            # -------------------------------------------
            cur.execute("""
                SELECT estado_id
                FROM habitacion
                WHERE numero_habitacion=%s
            """, (num_hab,))

            hab = cur.fetchone()

            if hab is None:
                QMessageBox.warning(
                    self, "Error",
                    "La habitación NO existe."
                )
                return

            estado_id = hab[0]
            if estado_id != 1:   # 1 = disponible
                QMessageBox.warning(
                    self, "Error",
                    "La habitación NO está disponible."
                )
                return

            # -------------------------------------------
            # Insertar reserva
            # -------------------------------------------
            cur.execute("""
                INSERT INTO reserva (
                    tiempo_max_cancelacion,
                    fecha_llegada,
                    fecha_salida,
                    tipo_documento,
                    numero_documento,
                    numero_habitacion
                ) VALUES (%s,%s,%s,%s,%s,%s)
            """, (
                tiempo_max,
                fecha_lleg,
                fecha_sal,
                tipo_doc,
                num_doc,
                num_hab
            ))

            self.ocupar_habitacion(cur, num_hab)

            conn.commit()
            QMessageBox.information(self, "OK", "Reserva creada correctamente.")

        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Error", str(e))

        finally:
            conn.close()

    def sincronizar_secuencia_reserva(self, cur):
        """
        Ajusta automáticamente la secuencia del IDENTITY de reserva
        si está desfasada, evitando errores de llave duplicada.
        """
        # 1. Obtener el ID máximo actual
        cur.execute("SELECT COALESCE(MAX(reserva_id), 0) FROM reserva;")
        max_id = cur.fetchone()[0]

        # 2. Obtener el valor actual de la secuencia
        cur.execute("""
            SELECT last_value
            FROM pg_sequences
            WHERE schemaname='public' AND sequencename='reserva_reserva_id_seq';
        """)
        seq_value = cur.fetchone()[0]

        # 3. Si la secuencia está atrasada, actualizarla
        if seq_value < max_id:
            cur.execute("""
                SELECT setval('reserva_reserva_id_seq', %s, true);
            """, (max_id,))

    def ocupar_habitacion(self, cur, num_hab):
        """
        Cambia el estado de la habitación a OCUPADA (estado_id = 2)
        """
        cur.execute("""
            UPDATE habitacion
            SET estado_id = 2
            WHERE numero_habitacion = %s
        """, (num_hab,))
