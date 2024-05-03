from sqlite3 import *
from sqlite3 import Error
from os import *
from tkinter import *
from tkinter import ttk
from msilib.schema import RadioButton

aken= Tk()
aken.title('PythonGuides')
aken.geometry('900x400')
aken['bg']='#ffc0cb'

#def Andmed (tabel:str):
#    con1=sqlite3.connect(dbpath)
#    cur1.execute(f"SELECT * FROM {tabel}")
#    cur1=con1.cursor()
#    rows = cur1.fetchall()
#    for row in rows:
#        print(row)
#        tree. insert("", END, values=row)
#    con1.close()

tree = ttk.Treeview(aken)
tree['columns']=('ID', 'Autor_id', 'Raamat_id', 'Zanr_id', 'Väljaandmise_kuupäev')
tree.column('#0', width=0, stretch=NO)
tree.column('ID', anchor=CENTER, width=150)
tree.column('Autor_id', anchor=CENTER, width=150)
tree.column('Raamat_id', anchor=CENTER, width=150)
tree.column('Zanr_id', anchor=CENTER, width=150)
tree.column('Väljaandmise_kuupäev', anchor=CENTER, width=150)

tree.heading('#0', text='', anchor=CENTER)
tree.heading('ID', text='Id', anchor=CENTER)
tree.heading('Autor_id', text='Autor', anchor=CENTER)
tree.heading('Raamat_id', text='Raamat', anchor=CENTER)
tree.heading('Zanr_id', text='Žanr', anchor=CENTER)
tree.heading('Väljaandmise_kuupäev', text='Väljaandmise kuupäev', anchor=CENTER)
tree.pack()


aken.mainloop()

def create_connect(path:str):             #path->путь
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



create_Raamatud_table="""
CREATE TABLE IF NOT EXISTS raamatud(
Raamat_id INTEGER PRIMARY KEY AUTOINCREMENT,
pealkiri TEXT NOT NULL,
valjaandmise_kuupäev DATE NOT NULL,
autor_id INTEGER,
zanr_id INTEGER,
FOREIGN KEY (autor_id) REFERENCES autorid (Autor_id),
FOREIGN KEY (zanr_id) REFERENCES zanrid (Zanr_id)
)
"""
insert_raamatud="""
INSERT INTO
raamatud(pealkiri,valjaandmise_kuupäev,Autor_id,Zanr_id)
VALUES
('Crooked House','24-09-2024'),
('Norwegian forest','15-12-2024'),
('Nightingale and rose','30-04-2024'),
('Twelve','09-10-2024')
"""



select_raamatud="SELECT * from raamatud"
select_raamatud_autorId="SELECT * from autorid"
select_raamatud_zanrId="SELECT * from zanrid"
select_raamatud_autorId="SELECT raamatud.pealkiri,raamatud.valjaandmise_kuupäev,autorid.autor_nimi from raamatud INNER JOIN autorid ON raamatud.Autor_id=autorid"
select_raamatud_zanrId="SELECT raamatud.pealkiri,raamatud.valjaandmise_kuupäev,zanrid.autor_nimi from raamatud INNER JOIN zanrid ON raamatud.Zanr_id=zanrid"



create_Autorid_table="""
CREATE TABLE IF NOT EXISTS autorid(
Autor_id INTEGER PRIMARY KEY AUTOINCREMENT,
autor_nimi TEXT NOT NULL,
autor_perenimi TEXT NOT NULL,
sünnikuupäev DATE NOT NULL
)
"""
insert_autorid="""
INSERT INTO
autorid(Autor_id,autor_nimi,autor_perenimi,sünnikuupäev)
VALUES
('Agatha','Christie','15-09-1890'),
('Haruki','Murakami','12-01-1949'),
('Oskar','Wilde','16-10-1854'),
('Alexander','Blok','28-11-1880')
"""



create_Zanrid_table="""
CREATE TABLE IF NOT EXISTS zanrid(
Zanr_id INTEGER PRIMARY KEY AUTOINCREMENT,
zanri_nimi TEXT NOT NULL
)
"""
insert_zanrid="""
INSERT INTO
zanrid(Zanr_id,zanri_nimi)
VALUES
('Detective novel'),
('Novel'),
('Fiction'),
('Poem')
"""




filename=path.abspath(__file__)
dbdir=filename.rstrip('AndmebaasiHaldamineRaamatukataloogis.py')
dbpath=path.join(dbdir,"data.db")
conn=create_connect(dbpath)

insert_raamatud=(input("Pealkiri : "),input("Autor Nimi : "),input("Autor Perenimi : "),int(input("Väljaandmise kuupäev : ")),input("Zanrid:"))
execute_query(conn, create_Raamatud_table)

execute_query(conn, create_Autorid_table)
execute_query(conn, create_Zanrid_table)
execute_query(conn, insert_raamatud)
execute_query(conn, insert_autorid)
execute_query(conn, insert_zanrid)



raamatud=execute_read_query(conn,select_raamatud)
print("Raamatud tabel 1 : ")
for raamat in raamatud:
    print(raamat)
autorid=execute_read_query(conn,select_raamatud_autorId)
print("Autor tabel 2 : ")
for auto in autorid:
    print(auto)
zanrid=execute_read_query(conn,select_raamatud_zanrId)
print("Zanr tabel 3 : ")
for zanr in zanrid:
    print(zanr)


#arvutada_nupp =RadioButton(aken, text="Lahendamine", font=("Impact", 20), command=Andmed)
#arvutada_nupp.grid(row=3, column=3, columnspan=4)

#graafiku_nupp =RadioButton(aken, text="Kuva graafik", font=("Impact", 20), command=Andmed)
#graafiku_nupp.grid(row=6, column=3, columnspan=4)