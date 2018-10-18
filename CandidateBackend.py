import sqlite3
import re

class Database:

    def __init__(self, db):
        self.conn=sqlite3.connect(db)
        self.cur=self.conn.cursor()

        sql = "CREATE TABLE IF NOT EXISTS candidate (id INTEGER PRIMARY KEY AUTOINCREMENT, name text, country text, prospective_role text, experience_years int, first_contacted date, linked_in text, contact_details text, skills text, notes text)"
        self.cur.execute(sql)
        self.conn.commit()

    def insert(self, name, country, prospective_role, experience_years, first_contacted, linked_in, contact_details, skills, notes):
        self.cur.execute("INSERT INTO candidate VALUES (NULL,?,?,?,?,?,?,?,?,?)", (name, country, prospective_role, experience_years, first_contacted, linked_in, contact_details, skills, notes))
        self.conn.commit()
        return self.cur.lastrowid

    def fetch_all(self):
        self.cur.execute("SELECT * FROM candidate")
        rows=self.cur.fetchall()
        return rows

    def search(self, keyword):
        sql = "SELECT * FROM candidate WHERE name LIKE ? OR country LIKE ? OR prospective_role LIKE ? OR first_contacted LIKE ? OR contact_details LIKE ? OR skills LIKE ? OR notes LIKE ?"
        like = '%' + keyword + '%'
        params = (like, like, like, like, like, like, like)
        self.cur.execute(sql, params)
        rows=self.cur.fetchall()
        return rows

    def delete(self, id):
        self.cur.execute("DELETE FROM candidate WHERE id=?", (id,))
        self.conn.commit()

    def update_field(self, id, column, value):
        column = re.sub(r'\W+', '', column)                     # Strip out anything that's not just a letter to prevent any malicious SQL
        sql = "UPDATE candidate SET %s=? WHERE id=?" % column   # Build an SQL statement with the given column name
        self.cur.execute(sql, (value, id))
        self.conn.commit()

    def update(self, id, name, country, prospective_role, experience_years, first_contacted, linked_in, contact_details, skills, notes):
        sql = "UPDATE candidate SET name=?, country=?, prospective_role=?, experience_years=?, first_contacted=?, linked_in=?, contact_details=?, skills=?, notes=? WHERE id=?"
        params = (name, country, prospective_role, experience_years, first_contacted, linked_in, contact_details, skills, notes, id)
        self.cur.execute(sql, params)
        self.conn.commit()

    def __del__(self):
        self.conn.close()


#insert("Purple Rain", "iOS", "Serbia", "www.queen.co.uk", "Message sent", 2015-05-11)
#delete(4)
#update(5, "The universe", "Android", "France", "www.treepeple.com", "Message sent", 2015-05-11)
#print(view())
#print(search(position="Android"))
