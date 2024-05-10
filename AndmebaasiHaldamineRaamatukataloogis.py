from sqlite3 import connect, Error
from tkinter import Tk, Button, Frame, CENTER, Entry, Label
from tkinter import ttk
from os import path

def create_connect(path:str):           
    connection=None 
    try: 
        connection=connect(path)
        print("Ühendus on olemas! ")
    except Error as e:
        print(f"Tekkis viga : {e}")
    return connection

def execute_query(connection,query):
    try:
        cursor=connection.cursor()
        cursor.execute(query)
        connection.commit()
        print("Tabel on loodud või andned on sisestatud")
    except Error as e:
        print(f"Tekkis viga : {e}")

def execute_read_query(connection,query):
    cursor=connection.cursor()
    result=None
    try:
        cursor.execute(query)
        result=cursor.fetchall()
        return result
    except Error as e:
        print(f"Tekkis viga : {e}")

def add_new_entry(window, fields, labels, insert_query, conn):
    def insert_data():
        data = [field.get() for field in fields]
        execute_query(conn, insert_query, data)
        window.destroy()

    window = Tk()
    window.title("Lisa uus kirje")
    
    for i, label_text in enumerate(labels):
        Label(window, text=label_text).grid(row=i, column=0)
        fields[i] = Entry(window)
        fields[i].grid(row=i, column=1)

    Button(window, text="Lisa", command=insert_data).grid(row=len(labels), columnspan=2)
    window.mainloop()

filename = path.abspath(__file__)
dbdir = path.dirname(filename)
dbpath = path.join(dbdir, "data.db")
conn = create_connect(dbpath)

aken = Tk()
aken.title('Raamatupood')
aken.geometry('900x400')
aken.iconbitmap('pearl.ico')
aken['bg'] = '#99e6ff'

def tabel_rramatuid(conn):
    def add_new_raamatud_entry():
        väljad = [Entry(window_raamatud) for _ in range(4)]
        märgistama = ["Pealkiri", "Valjaandmise kuupäev", "Autori nimi", "Zanri nimi"]
        insert_query = "INSERT INTO raamatud (pealkiri, valjaandmise_kuupäev, autor_id, zanr_id) VALUES (?, ?, ?, ?)"
        add_new_entry(window_raamatud, väljad, märgistama, insert_query, conn)

    window_raamatud = Tk()
    tree = ttk.Treeview(window_raamatud)
    tree = ttk.Treeview(window_raamatud, column=("Raamat_id", "pealkiri", "valjaandmise_kuupäev", "autor_nimi", "zanri_nimi"), show="headings")
    tree.heading('Raamat_id', text='Raamat_id', anchor=CENTER)
    tree.heading('pealkiri', text='Pealkiri', anchor=CENTER)
    tree.heading('valjaandmise_kuupäev', text='Valjaandmise kuupäev', anchor=CENTER)
    tree.heading('autor_nimi', text='Autor nimi', anchor=CENTER)
    tree.heading('zanri_nimi', text='Zanri nimi', anchor=CENTER)

    create_Raamatud_table = """
    CREATE TABLE IF NOT EXISTS raamatud(
    Raamat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    pealkiri TEXT NOT NULL,
    valjaandmise_kuupäev DATE NOT NULL,
    autor_id INTEGER,
    zanr_id INTEGER,
    UNIQUE (Raamat_id)
    FOREIGN KEY (autor_id) REFERENCES autorid (Autor_id),
    FOREIGN KEY (zanr_id) REFERENCES zanrid (Zanr_id)
    )
    """
    insert_raamatud = """
    INSERT INTO
    raamatud(pealkiri, valjaandmise_kuupäev, autor_id, zanr_id)
    VALUES
    ('Crooked House', '2024-09-24', 1, 1),
    ('Norwegian forest', '2024-12-15', 2, 2),
    ('Nightingale and rose', '2024-04-30', 3, 3),
    ('Twelve', '2024-10-09', 4, 4)
    """
    
    execute_query(conn, create_Raamatud_table)
    execute_query(conn, insert_raamatud)

    try:
        read = execute_read_query(conn, "SELECT raamatud.Raamat_id, raamatud.pealkiri, raamatud.valjaandmise_kuupäev, autorid.autor_nimi, zanrid.zanri_nimi FROM raamatud INNER JOIN autorid ON raamatud.autor_id = autorid.Autor_id INNER JOIN zanrid ON raamatud.zanr_id = zanrid.Zanr_id")
        for row in read:
            tree.insert("", "end", values=row)
    except Error as e:
        print(f"Tekkis viga : {e}")

    Button(window_raamatud, text="Lisa uus kirje",bg="#b399ff", command=add_new_raamatud_entry).pack(pady=5)
    tree.pack()
    window_raamatud.mainloop()



def tabel_aautorid(conn):
    def add_new_autorid_entry():
        väljad = [Entry(window_aautorid) for _ in range(3)]
        märgistama = ["Autori nimi", "Autori perenimi", "Sünnikuupäev"]
        insert_query = "INSERT INTO autorid (autor_nimi, autor_perenimi, sünnikuupäev) VALUES (?, ?, ?)"
        add_new_entry(window_aautorid, väljad, märgistama, insert_query, conn)

    window_aautorid = Tk()
    tree = ttk.Treeview(window_aautorid)
    tree = ttk.Treeview(window_aautorid, column=("Autor_id", "autor_nimi", "autor_perenimi", "sünnikuupäev"), show="headings")
    tree.heading('Autor_id', text='Autor_id', anchor=CENTER)
    tree.heading('autor_nimi', text='Autor nimi',anchor=CENTER)
    tree.heading('autor_perenimi', text='Autor perenimi', anchor=CENTER)
    tree.heading('sünnikuupäev', text='Sünnikuupäev', anchor=CENTER)

    create_Autorid_table = """
    CREATE TABLE IF NOT EXISTS autorid(
    Autor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    autor_nimi TEXT NOT NULL,
    autor_perenimi TEXT NOT NULL,
    sünnikuupäev DATE NOT NULL,
    UNIQUE (Autor_id)
    )
    """
    insert_autorid = """
    INSERT INTO
    autorid(autor_nimi, autor_perenimi, sünnikuupäev)
    VALUES
    ('Agatha', 'Christie', '1890-09-15'),
    ('Haruki', 'Murakami', '1949-01-12'),
    ('Oskar', 'Wilde', '1854-10-16'),
    ('Alexander', 'Blok', '1880-11-28')
    """

    execute_query(conn, create_Autorid_table)
    execute_query(conn, insert_autorid)

    try:
        read = execute_read_query(conn, "SELECT * from autorid")
        for row in read:
            tree.insert("", "end", values=row)
    except Error as e:
        print(f"Tekkis viga : {e}")

    Button(window_aautorid, text="Lisa uus kirje",bg="#b399ff", command=add_new_autorid_entry).pack(pady=5)
    tree.pack()
    window_aautorid.mainloop()

def tabel_zzanrid(conn):
    def lisa_uus_zanrid_entry():
        väljad = [Entry(window_zzanrid) for _ in range(1)]
        märgistama = ["Zanri nimi"]
        insert_query = "INSERT INTO zanrid (zanri_nimi) VALUES (?)"
        add_new_entry(window_zzanrid, väljad, märgistama, insert_query, conn)

    window_zzanrid = Tk()
    tree = ttk.Treeview(window_zzanrid)
    tree = ttk.Treeview(window_zzanrid, column=("Zanr_id", "zanri_nimi"), show="headings")
    tree.heading('Zanr_id', text='Zanr_id', anchor=CENTER)
    tree.heading('zanri_nimi', text='Zanri nimi', anchor=CENTER)

    create_Zanrid_table = """
    CREATE TABLE IF NOT EXISTS zanrid(
    Zanr_id INTEGER PRIMARY KEY AUTOINCREMENT,
    zanri_nimi TEXT NOT NULL
    UNIQUE (Zanr_id)
    )
    """
    insert_zanrid = """
    INSERT INTO
    zanrid(zanri_nimi)
    VALUES
    ('Detective novel'),
    ('Novel'),
    ('Fiction'),
    ('Poem')
    """

    execute_query(conn, create_Zanrid_table)
    execute_query(conn, insert_zanrid)

    try:
        read = execute_read_query(conn, "SELECT * from zanrid")
        for row in read:
            tree.insert("", "end", values=row)
    except Error as e:
        print(f"Tekkis viga : {e}")

    Button(window_zzanrid, text="Lisa uus kirje",bg="#b399ff", command=lisa_uus_zanrid_entry).pack(pady=5)
    tree.pack()
    window_zzanrid.mainloop()

f = Frame(aken)
raamatu_nupp = Button(f, text="Raamatuid", font=("Algerian", 20),bg="#99ccff", command=lambda: tabel_rramatuid(conn)) 
raamatu_nupp.grid(row=3, column=3, columnspan=4)

autori_nupp = Button(f, text="Autorid", font=("Algerian", 20),bg="#99b3ff", command=lambda: tabel_aautorid(conn)) 
autori_nupp.grid(row=5, column=3, columnspan=4)

zanri_nupp = Button(f, text="Zanrid", font=("Algerian", 20),bg="#9999ff", command=lambda: tabel_zzanrid(conn)) 
zanri_nupp.grid(row=7, column=3, columnspan=4)

f.pack()
aken.mainloop()
