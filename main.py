import sqlite3
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QLineEdit
import datetime

class Lagerverwaltung:

    def __init__(self):
        self.con = sqlite3.connect("management.db")
        self.cur = self.con.cursor()

    def create_table(self):
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS LAGERVERWALTUNG(
            Datum DATE
            Bezeichnung TEXT,
            Typ TEXT,
            Menge INT,
            Raum TEXT,
            Schrank TEXT,
            CONSTRAINT Datum_unique UNIQUE (Datum));
            CONSTRAINT Bezeichnung_unique UNIQUE (Bezeichnung));
            CONSTRAINT Typ_unique UNIQUE (Typ));
            CONSTRAINT Menge_unique UNIQUE (Menge));
            CONSTRAINT Raum_unique UNIQUE (Raum));
            CONSTRAINT Schrank_unique UNIQUE (Schrank));"""
        )
        self.con.commit()

    def insert_data(self, Datum, Bezeichnung, Typ, Menge, Raum, Schrank):
        # Überprüfen, ob der Artikel bereits existiert
        self.cur.execute("SELECT Name FROM LAGERVERWALTUNG WHERE Name=?", (Datum,Bezeichnung,Typ,Menge,Raum,Schrank ))
        existing_row = self.cur.fetchone()
        if existing_row:
            print(f"Der Artikel '{Typ}' existiert bereits im Lager.")
        else:
            self.cur.execute(
                """INSERT INTO LAGERVERWALTUNG (Name, Raum, Schrank)
                VALUES (?, ?, ?)""", (Datum, Bezeichnung, Typ, Menge, Raum, Schrank)
            )
            self.con.commit()
            print(f"Der Artikel '{Bezeichnung}' wurde erfolgreich hinzugefügt.")

    def insert_multiple_data(self, data):
        """
        Insert multiple records at once
        data: List of tuples (Datum, Bezeichnung, Typ, Menge, Raum, Schrank)
        """
        for item in data:
            self.name = item[0]
            self.insert_data(*item)

    def retrieve_data(self):
        self.cur.execute("SELECT * FROM LAGERVERWALTUNG")
        rows = self.cur.fetchall()
        for row in rows:
            print(row)

    def close_connection(self):
        self.con.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lagerverwaltung")
        self.setGeometry(300, 300, 600, 400)

        self.lagerverwaltung = Lagerverwaltung()

        self.initUI()

    def initUI(self):
        # Hauptwidget erstellen
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Layouts erstellen
        main_layout = QVBoxLayout()
        table_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        # Suchfeld erstellen
        search_field = QLineEdit()
        search_field.setPlaceholderText("Suchen...")

        # Buttons erstellen
        btn_add = QPushButton("Hinzufügen")
        btn_edit = QPushButton("Bearbeiten")
        btn_delete = QPushButton("Löschen")
        btn_exit = QPushButton("Beenden")

        # Button-Layout konfigurieren
        button_layout.addWidget(btn_add)
        button_layout.addWidget(btn_edit)
        button_layout.addWidget(btn_delete)
        button_layout.addStretch()  # Stretch, um Suchfeld rechts zu halten
        button_layout.addWidget(search_field)
        button_layout.addWidget(btn_exit)

        # Tabellenwidget erstellen
        table_widget = QTableWidget()
        table_widget.setColumnCount(6)
        table_widget.setHorizontalHeaderLabels(["Datum", "Bezeichnung", "Typ", "Menge", "Raum", "Schranknummer"])

        # Tabelle in Layout einfügen
        table_layout.addWidget(QLabel("Lagerverzeichnis:"))
        table_layout.addWidget(table_widget)

        # Hauptlayout konfigurieren
        main_layout.addLayout(button_layout)
        main_layout.addLayout(table_layout)

        # Hauptwidget-Layout einstellen
        main_widget.setLayout(main_layout)

        # Signale und Slots verbinden
        btn_add.clicked.connect(self.add_data)
        btn_edit.clicked.connect(self.edit_data)
        btn_delete.clicked.connect(self.delete_data)
        btn_exit.clicked.connect(self.close)

        self.show()

    def add_data(self):
        # Hier könntest du die Eingabefelder für das Hinzufügen von Daten anzeigen
        pass

    def edit_data(self):
        # Hier könntest du die Bearbeitung von Daten implementieren, z.B. indem du die ausgewählte Zeile der Tabelle bearbeitbar machst
        pass

    def delete_data(self):
        # Hier könntest du die ausgewählte Zeile der Tabelle löschen
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
