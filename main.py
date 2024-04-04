import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, \
    QLineEdit, QTextEdit, QMessageBox, QTableWidgetItem, QTableWidget, QDialog, QFormLayout
from PyQt5.QtGui import QPixmap


class Lagerverwaltung:

    def __init__(self):
        self.connection = sqlite3.connect("C:\\Projekte\\Python\\Lagerverwaltung\\lagerverwaltung.db")
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS artikel (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                bezeichnung TEXT,
                                typ TEXT,
                                menge INTEGER,
                                raum TEXT,
                                schrank INTEGER
                                )""")
        self.connection.commit()

    def insert_artikel(self, bezeichnung, typ, menge, raum, schrank):
        self.cursor.execute("INSERT INTO artikel (bezeichnung, typ, menge, raum, schrank) VALUES (?, ?, ?, ?, ?)",
                            (bezeichnung, typ, menge, raum, schrank))
        self.connection.commit()

    def update_artikel(self, artikel_id, bezeichnung, typ, menge, raum, schrank):
        self.cursor.execute("UPDATE artikel SET bezeichnung=?, typ=?, menge=?, raum=?, schrank=? WHERE id=?",
                            (bezeichnung, typ, menge, raum, schrank, artikel_id))
        self.connection.commit()

    def delete_artikel(self, artikel_id):
        self.cursor.execute("DELETE FROM artikel WHERE id=?", (artikel_id,))
        self.connection.commit()

    def search_artikel(self, bezeichnung):
        self.cursor.execute("SELECT * FROM artikel WHERE bezeichnung LIKE ?", ('%' + bezeichnung + '%',))
        return self.cursor.fetchall()

    def get_all_artikel(self):
        self.cursor.execute("SELECT * FROM artikel")
        return self.cursor.fetchall()


class LagerGUI(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lagerverwaltung")
        self.setGeometry(100, 100, 800, 600)

        self.lagerverwaltung = Lagerverwaltung()

        self.initUI()

    def initUI(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        foto_button = QPushButton("Foto anzeigen")
        foto_button.setFixedSize(100, 30)  # Set width to 100 pixels and height to 30 pixels
        foto_button.clicked.connect(self.show_image)
        main_layout.addWidget(foto_button)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(6)
        self.table_widget.setHorizontalHeaderLabels(["ID", "Bezeichnung", "Typ", "Menge", "Raum", "Schrank"])
        self.update_table()

        main_layout.addWidget(self.table_widget)

        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)

        self.search_field = QLineEdit()
        button_layout.addWidget(self.search_field)

        search_button = QPushButton("Suchen")
        search_button.clicked.connect(self.search_artikel)
        button_layout.addWidget(search_button)

        add_button = QPushButton("Hinzufügen")
        add_button.clicked.connect(self.add_artikel)
        button_layout.addWidget(add_button)

        edit_button = QPushButton("Bearbeiten")
        edit_button.clicked.connect(self.edit_artikel)
        button_layout.addWidget(edit_button)

        delete_button = QPushButton("Löschen")
        delete_button.clicked.connect(self.delete_artikel)
        button_layout.addWidget(delete_button)

    def update_table(self):
        self.table_widget.setRowCount(0)
        artikel_list = self.lagerverwaltung.get_all_artikel()
        for row_number, row_data in enumerate(artikel_list):
            self.table_widget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table_widget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def add_artikel(self):
        dialog = ArtikelDialog()
        if dialog.exec_():
            bezeichnung, typ, menge, raum, schrank = dialog.get_data()
            self.lagerverwaltung.insert_artikel(bezeichnung, typ, menge, raum, schrank)
            self.update_table()

    def edit_artikel(self):
        selected_row = self.table_widget.currentRow()
        if selected_row != -1:
            artikel_id = int(self.table_widget.item(selected_row, 0).text())
            dialog = ArtikelDialog(edit_mode=True)
            dialog.set_data(*self.lagerverwaltung.get_all_artikel()[selected_row][1:])
            if dialog.exec_():
                bezeichnung, typ, menge, raum, schrank = dialog.get_data()
                self.lagerverwaltung.update_artikel(artikel_id, bezeichnung, typ, menge, raum, schrank)
                self.update_table()
        else:
            QMessageBox.warning(self, "Warnung", "Bitte wählen Sie einen Artikel zum Bearbeiten aus.")

    def delete_artikel(self):
        selected_row = self.table_widget.currentRow()
        if selected_row != -1:
            artikel_id = int(self.table_widget.item(selected_row, 0).text())
            reply = QMessageBox.question(self, 'Löschen', 'Möchten Sie den ausgewählten Artikel löschen?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.lagerverwaltung.delete_artikel(artikel_id)
                self.update_table()
        else:
            QMessageBox.warning(self, "Warnung", "Bitte wählen Sie einen Artikel zum Löschen aus.")

    def search_artikel(self):
        search_text = self.search_field.text()
        if search_text.strip() != "":
            artikel_list = self.lagerverwaltung.search_artikel(search_text)
            self.table_widget.setRowCount(0)
            for row_number, row_data in enumerate(artikel_list):
                self.table_widget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.table_widget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        else:
            self.update_table()

    def show_image(self):
        # Display image in a message box
        image_path = "C:\\Projekte\\Python\\Lagerverwaltung\\Pictures\\overview.jpg"
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            QMessageBox.warning(self, "Warnung", "Das Bild konnte nicht gefunden werden.")

        else:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Foto anzeigen")
            msg_box.setIconPixmap(pixmap)
            msg_box.exec_()

class ArtikelDialog(QDialog):
    def __init__(self, edit_mode=False, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Artikel")
        self.setModal(True)

        layout = QFormLayout()

        self.bezeichnung_edit = QLineEdit()
        layout.addRow("Bezeichnung:", self.bezeichnung_edit)

        self.typ_edit = QLineEdit()
        layout.addRow("Typ:", self.typ_edit)

        self.menge_edit = QLineEdit()
        layout.addRow("Menge:", self.menge_edit)

        self.raum_edit = QLineEdit()
        layout.addRow("Raum:", self.raum_edit)

        self.schrank_edit = QLineEdit()
        layout.addRow("Schrank:", self.schrank_edit)

        self.btn_ok = QPushButton("OK")
        self.btn_ok.clicked.connect(self.accept)
        layout.addWidget(self.btn_ok)

        self.setLayout(layout)

        self.edit_mode = edit_mode

    def set_data(self, bezeichnung, typ, menge, raum, schrank):
        self.bezeichnung_edit.setText(bezeichnung)
        self.typ_edit.setText(typ)
        self.menge_edit.setText(str(menge))
        self.raum_edit.setText(raum)
        self.schrank_edit.setText(str(schrank))

    def get_data(self):
        return (
            self.bezeichnung_edit.text(),
            self.typ_edit.text(),
            int(self.menge_edit.text()),
            self.raum_edit.text(),
            int(self.schrank_edit.text())
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LagerGUI()
    window.show()
    sys.exit(app.exec_())
