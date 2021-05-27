import sqlite3
import collections

#crear la conexion
def sql_connection():
    try:
        con = sqlite3.connect('SQLite3/test.sqlite3')
        return con
    except Error:
        print(Error)

#consulta el año que mas se estreno peliculas
def sql_yearT(con):
    print("Años con mas peliculas")
    cursorObj = con.cursor()
    cursorObj.execute('SELECT year, COUNT(year) total FROM movies GROUP BY year ORDER by total DESC;')
    row= cursorObj.fetchall()
    global numero
    numero=0
    print("Año:","Total:")
    while  (numero<3):
        print(row[numero])
        numero+=1
    con.commit()
    
#consulta 5 mejores actores
def sql_fiveA(con):
    print("Actores con la trayectoria mas larga")
    lis=list()
    cursorObj = con.cursor()
    cursorObj.execute('SELECT casting from movies;')
    rows= cursorObj.fetchall()
    con.commit()
    global cont
    cont=0;
    for row in rows:
        actores=row[0].split("-")
        for actor in actores:
            cursorObj1 = con.cursor()
            if(actor.find("'")>0 or actor.find("'")==0 ):
                actor=actor.replace("'"," ");
            if(len(actor)>12):
                cursorObj1.execute("""SELECT year FROM movies where casting LIKE '"""+str(actor)+"""%';""")
                actorY=cursorObj1.fetchall()
                if(len(actorY)!=0):
                    va1=len(actorY)-1
                    va2=int(float(actorY[0][0])) 
                    va3=int(float(actorY[va1][0]))
                    valor=va3-va2        
                    if(lis.count((valor,actor))==0):
                        lis.append((valor,actor))
                    cont+=1
                con.commit()    
        if(cont==1000):
            lis=sorted(lis, key=lambda a : a[0],reverse=True)
            lis=[lis[0],lis[1],lis[2],lis[3],lis[4]]
            cont=0
    lis=sorted(lis, key=lambda a : a[0],reverse=True)
    global numero
    numero=0
    while(numero<5):
        print(lis[numero],(numero+1))
        numero+=1
        
#consulta ordenar por genero y los 3 mejores de cada genero
def sql_genresA(con):
    print("Ranking de generos y actores mas populares en cada genero")
    cursorObj = con.cursor()
    cursorObj.execute('SELECT genres,count(genres) total from movies  GROUP BY genres ORDER by total DESC LIMIT 20;')
    generos= cursorObj.fetchall()
    con.commit()
    global cont1
    cont1=0;
    for genero in generos:
        print((cont1+1),genero)
        lis=list()
        cursorObj = con.cursor()
        cursorObj.execute('SELECT casting from movies;')
        rows= cursorObj.fetchall()
        con.commit()
        global cont
        cont=0;
        for row in rows:
            actores=row[0].split("-")
            for actor in actores:
                cursorObj1 = con.cursor()
                if(actor.find("'")>0 or actor.find("'")==0 ):
                    actor=actor.replace("'"," ");
                if(len(actor)>12):
                    cursorObj1.execute("""SELECT year FROM movies where casting LIKE '"""+str(actor)+"""%' AND genres='"""+genero[0]+"""';""")
                    actorY=cursorObj1.fetchall()
                    if(len(actorY)!=0):
                        va1=len(actorY)-1
                        va2=int(float(actorY[0][0])) 
                        va3=int(float(actorY[va1][0]))
                        valor=va3-va2        
                        if(lis.count((valor,actor))==0):
                            lis.append((valor,actor))
                        cont+=1
                    con.commit()    
            if(cont==1000):
                lis=sorted(lis, key=lambda a : a[0],reverse=True)
                lis=[lis[0],lis[1],lis[2],lis[3],lis[4]]
                cont=0
        lis=sorted(lis, key=lambda a : a[0],reverse=True)
        global numero
        numero=0
        while(numero<3):
            print("  ",(numero+1),"-",lis[numero])
            numero+=1
        cont1+=1
   
#main
con = sql_connection()

#sql_yearT(con)   #consulto los años con mas publicacion

#las siguientes consultas tiene una duracion mas larga a trabajar con +27000 datos
#sql_fiveA(con)   #consulta 5 mejores actores
#sql_genresA(con) #consulta ordenar por genero y los 3 mejores de cada genero

#cierro connect
con.close
