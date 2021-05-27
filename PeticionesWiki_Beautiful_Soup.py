import sqlite3
from bs4 import BeautifulSoup
import requests
import time

#crear la conexion
def sql_connection():
    try:
        con = sqlite3.connect('SQLite3/test.sqlite3')
        return con
    except Error:
        print(Error)

#consulta a la base de datos
def sql_fetch(con):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * from movies where year= "2015"')
    rows= cursorObj.fetchall()
    for row in rows:
        print(row[0])
        print()
    con.commit()    
        
#consulta de agregar columnas       
def sql_addColumn(con):
    cursorObj = con.cursor()
    cursorObj.execute("SELECT name from PRAGMA_TABLE_INFO('movies');")
    rows= cursorObj.fetchall()
    global ban
    ban=0
    lista=[]
    for row in rows:
        if(row[0]=="director" or row[0]=="studio"):
            ban+=1
            lista.append(ban)
    if(ban==0):
        cursorObj.execute('ALTER TABLE movies ADD director text NOT NULL DEFAULT "no data";')
        cursorObj.execute('ALTER TABLE movies ADD studio text NOT NULL DEFAULT "no data";')
    if(ban==1):
        if(lista[0]==1):
            cursorObj.execute('ALTER TABLE movies ADD director text NOT NULL DEFAULT "no data";')
        if(lista[0]==2):
            cursorObj.execute('ALTER TABLE movies ADD studio text NOT NULL DEFAULT "no data";')
    con.commit()
    
#consulta de cambio
def sql_update(con,task):
    cursorObj = con.cursor()
    cursorObj.execute("""
    UPDATE movies 
       SET director = ? ,
           studio= ? 
    WHERE title= ? ;
    """,task)
    con.commit()


#peticion get a wiki-año    
def consultaWiki(con,year):
    page=requests.get('https://en.wikipedia.org/wiki/List_of_American_films_of_'+str(year))
    soup=BeautifulSoup(page.text,'html.parser')
    table_items=soup.find_all('table')
    global numero
    global nombre
    global director
    global estudio
    numero=0
    nombre=""
    director=""
    estudio=""
    for table in table_items:
        th=table.find_all('th')
        if(len(th)!=15 and len(th)>0 and (len(th[0].text)==6 or len(th[0].text)==8)):
            #peliculas <  2000
            if(len(th[0].text)==6):
                numero=0
                td=table.find_all('td')
                #print(td)
                for item in td:
                     numero+=1
                     if(numero==1):
                         nombre=item.text
                     if(numero==2):
                         director=item.text
                     if(numero%5==0):
                         estudio=item.text
                         if(len(estudio)>1 and len(director)>1):   
                            sql_update(con,(director,estudio,nombre));
                            numero=0
                            nombre=""
                            director=""
                            estudio=""
                            
            #peliculas > 2000            
            if(len(th[0].text)==8):
                numero=0
                td=table.find_all('td')
                for item in td:
                    if(len(item.text)>3 and (item.text.find("[")==-1)):
                        numero+=1
                        if(numero==1):
                            nombre=item.text
                        if(numero==2):
                            estudios=item.text.split("/")
                            if(len(estudios)>1):
                                estudio='-'.join(str(e) for e in estudios)
                            else:
                                estudio=estudios[0]   
                        if(numero==3):
                            directors=item.text.split("(director")
                            director=directors[0]   
                            sql_update(con,(director,estudio,nombre));
                            numero=0
                            nombre=""
                            director=""
                            estudio=""
                    elif(len(item.text)<4):
                         numero=0
                         nombre=""
                         director=""
                         estudio=""
              
                
#main
con = sql_connection()
sql_addColumn(con) #creo las dos columnas
consultaWiki(con,1960) #cargo los datos del año

#cierro connect
con.close
