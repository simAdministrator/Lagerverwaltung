import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog


class Lagerverwaltung:

    def __init__(self):
        self.con = sqlite3.connect("management.db")
        self.cur = self.con.cursor()

    def create_table(self):
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS LAGERVERWALTUNG(
            Name TEXT,
            Raum TEXT,
            Schrank TEXT,
            CONSTRAINT name_unique UNIQUE (Name));"""
        )
        self.con.commit()

    def insert_data(self, name, raum, schrank):
        # Überprüfen, ob der Artikel bereits existiert
        self.cur.execute("SELECT Name FROM LAGERVERWALTUNG WHERE Name=?", (name,))
        existing_row = self.cur.fetchone()
        if existing_row:
            print(f"Der Artikel '{name}' existiert bereits im Lager.")
        else:
            self.cur.execute(
                """INSERT INTO LAGERVERWALTUNG (Name, Raum, Schrank)
                VALUES (?, ?, ?)""", (name, raum, schrank)
            )
            self.con.commit()
            print(f"Der Artikel '{name}' wurde erfolgreich hinzugefügt.")

    def insert_multiple_data(self, data):
        """
        Insert multiple records at once
        data: List of tuples (name, raum, schrank)
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


class GUI(Lagerverwaltung):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.master.title("Lagerverwaltung")

        self.entry_listbox = tk.Listbox(master)
        self.entry_listbox.pack(padx=30, pady=30)

        add_button = tk.Button(master, text="Hinzufügen", command=self.add_entry)
        add_button.pack(padx=10, pady=5, fill=tk.X)

        delete_button = tk.Button(master, text="Löschen", command=self.delete_entry)
        delete_button.pack(padx=10, pady=5, fill=tk.X)

        show_image_button = tk.Button(master, text="Bild anzeigen", command=self.show_image)
        show_image_button.pack(padx=10, pady=5, fill=tk.X)

        close_button = tk.Button(master, text="Fenster schließen", command=master.quit)
        close_button.pack(padx=10, pady=5, fill=tk.X)

    def add_entry(self):
        entry = simpledialog.askstring("Neuen Eintrag hinzufügen", "Geben Sie den neuen Eintrag ein:")
        if entry:
            self.insert_data(entry, "", "")  # Hier werden die Daten direkt in die Datenbank eingefügt
            self.update_listbox()

    def delete_entry(self):
        selected_index = self.entry_listbox.curselection()
        if selected_index:
            entry_name = self.entry_listbox.get(selected_index)
            self.cur.execute("DELETE FROM LAGERVERWALTUNG WHERE Name=?", (entry_name,))
            self.con.commit()
            self.update_listbox()

    def show_image(self):
        # Hier könntest du Code einfügen, um ein Bild anzuzeigen
        messagebox.showinfo("Bild anzeigen", "Hier würde das Bild angezeigt werden.")

    def update_listbox(self):
        self.entry_listbox.delete(0, tk.END)
        self.cur.execute("SELECT Name FROM LAGERVERWALTUNG")
        rows = self.cur.fetchall()
        for row in rows:
            self.entry_listbox.insert(tk.END, row[0])


def main():
    root = tk.Tk()
    gui = GUI(root)
    gui.update_listbox()  # Initialisiere die Liste beim Start der Anwendung
    root.mainloop()


if __name__ == "__main__":
    main()
