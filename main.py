import sqlite3

class Lagerverwaltung:

    def __init__(self):
        self.con = sqlite3.connect("lagerverwaltung.db")
        self.cur = self.con.cursor()
        self.create_table()

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
            name = item[0]
            self.insert_data(*item)

    def retrieve_data(self):
        self.cur.execute("SELECT * FROM LAGERVERWALTUNG")
        rows = self.cur.fetchall()
        for row in rows:
            print(row)

    def close_connection(self):
        self.con.close()

if __name__ == "__main__":
    lager = Lagerverwaltung()
    lager.insert_multiple_data([
        ("WC-Papier", "Sitzungszimmer/Kopierraum", "gegenüber Fenster"),
        ("Abfallsaecke 35l", "Sitzungszimmer/Kopierraum", "gegenueber Fenster"),
        ("Abfallsaecke 110l", "Sitzungszimmer/Kopierraum", "gegenueber Fenster"),
        ("Abfallmarken 35l", "Sitzungszimmer/Kopierraum", "gegenueber Fenster"),
        ("Abfallmarken 110l", "Sitzungszimmer/Kopierraum", "gegenueber Fenster")
    ])
    lager.retrieve_data()
    lager.close_connection()

