import sqlite3
import json
from sqlite3 import Error

#crear la conexion
def sql_connection():
    try:
        con = sqlite3.connect('SQLite3/test.sqlite3')
        return con
    except Error:
        print(Error)

#codigo crear tabla
def sql_table(con):
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE IF NOT EXISTS movies( title text, year INTEGER, casting text, genres text)")
    con.commit()


#codigo agregar tabla
def sql_insert(con,title,year,cast,genres):
    cursorObj = con.cursor()
    cursorObj.execute("INSERT INTO movies (title,year,casting,genres)VALUES( ?,?,?,?)",(title,year,cast,genres))
    con.commit()

#creao tabla
con = sql_connection()
sql_table(con)

#cargo datos
global numero
numero=0
with open('movies.json',encoding="utf8") as f :
    data = json.load(f)
    for item in data:
        if(item['cast']!=[] and item['genres']!=[] and item['year']!='' and item['title']!=''):
           cast='-'.join(str(e) for e in data[numero]['cast'])
           genres='-'.join(str(e) for e in data[numero]['genres'])
           sql_insert(con,item['title'],item['year'],cast,genres)
        numero+=1;

#cierro connect
con.close
