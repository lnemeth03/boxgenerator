import os
import trimesh
import numpy as np
import tkinter as tk
import math
from tkinter import ttk

#Beállítások
#megnyit =  #Megnyitja-e a generált fájlt
x = 150 #A doboz szélessége
y = 200 #A doboz mélysége
z = 50 #A doboz magassága
bz =45 #A doboz belső falainak magassága
ykomponens = 2 #A komponensek száma az y tengely mentén
xkomponens = 1 #A komponensek száma az x tengely mentén
kfal = 2 #Külső falak vastagsága
bfal =  1 #Belső falak vastagsága
simasag = 10 #A kivágás simasága egy iterációs szám, hogy hány részből álljon a lekerekítés
kerekites = True #Kerekítés a generálásnál

# Csak, hogy vscode alatt is ugyanabba a mappába generáljon
os.chdir(os.path.dirname(os.path.abspath(__file__)))
def errorwindow(message):
    #Error window
    error=tk.Tk()
    error.title("Error")
    errorlabel = tk.Label(error, text=message,anchor="e")
    errorlabel.pack()
    error.mainloop()

def boxgenerator():
    #Értékek beolvasása
    try:
        x = float(xvalue.get())
        y = float(yvalue.get())
        z = float(zvalue.get())
        bz = float(bzvalue.get())
        ykomponens = int(ykomponensvalue.get())
        xkomponens = int(xkomponensvalue.get())
        kfal = float(kfalvalue.get())
        bfal = float(bfalvalue.get())
        megnyit = megnyit2.get()
        kerekites = kerekites2.get()
        simasag = int(simasagvalue.get())
        
        #Értékek ellenőrzése, hogy valóban dobozt generálunk-e  (kikommentelhetö, de akkor furcsa alakzatokat is lehet generálni)
        if bz > z:
            errorwindow("A belső falak magassága nem lehet nagyobb a doboz magasságánál!")
            return
        if 2*kfal > x or 2*kfal > y:
            errorwindow("A külső falak vastagsága nem lehet nagyobb a doboz méretének felénél!")
            return
        if kfal>z:
            errorwindow("A külső falak vastagsága nem lehet nagyobb a doboz magasságánál!")
            return
        if bfal*xkomponens+2*kfal>x:
            errorwindow("A falak vastagsága nem lehet nagyobb a doboz szélességénél!")
            return
        if bfal*ykomponens+2*kfal>y:
            errorwindow("A falak vastagsága nem lehet nagyobb a doboz mélységénél!")
            return
        
    except Exception:
        errorwindow("Hibás argumentumok!")
        return
    #Megadott méretű doboz generálása
    points = [[x,y,z], [x,y,0], [x,0,z], [x,0,0], [0,y,z], [0,y,0], [0,0,z], [0,0,0]]
    cloud = trimesh.points.PointCloud(points)
    hull_mesh = cloud.convex_hull
    
    #A doboz széleinek kerekítése
    if kerekites:
        #A négy külső falat egyszerre vágjuk ki
        #Vastagságnyit kerekítünk
        points = [[x,y,z], [x,y,z-kfal], [x,0,z], [x,0,z-kfal], [0,y,z], [0,y,z-kfal], [0,0,z], [0,0,z-kfal]]
        cloud4 = trimesh.points.PointCloud(points)
        hull_mesh4 = cloud4.convex_hull
        hull_mesh = hull_mesh.difference(hull_mesh4)
        
        #Kitöltjük "piramis" szerűen a kivágást
        for i in range(1,simasag):
            x3 = x
            y3 = y
            seg=i*kfal/simasag
            z3=z-kfal+seg
            poinst3 = [[x-seg,y-seg,z3], [x-seg,y-seg,z-kfal], [x-seg,seg,z3], [x-seg,seg,z-kfal], [seg,y-seg,z3], [seg,y-seg,z-kfal], [seg,seg,z3], [seg,seg,z-kfal]]
            cloud3 = trimesh.points.PointCloud(poinst3)
            hull_mesh3 = cloud3.convex_hull
            hull_mesh = hull_mesh+hull_mesh3
    
    #Doboz belsejének törlése (külső falak megtartásával)
    x2 = x - kfal
    y2 = y - kfal
    z2 = z #A tetejét el kell érnie a kivágásnak
    poinst2 = [[x2,y2,z2], [x2,y2,kfal], [x2,kfal,z2], [x2,kfal,kfal], [kfal,y2,z2], [kfal,y2,kfal], [kfal,kfal,z2], [kfal,kfal,kfal]]
    cloud2 = trimesh.points.PointCloud(poinst2)
    hull_mesh2 = cloud2.convex_hull
    hull_mesh = hull_mesh.difference(hull_mesh2)
    xkomponens*((x-2*kfal)/xkomponens+(3*bfal/xkomponens))
    
    
    #Belső falak generálása x mentén
    for i in range(1,xkomponens):
        x3 = i*x2/xkomponens
        y3 = y2
        z3 = bz
        bfal2=bfal/2
        kfal2=kfal/2
        poinst3 = [[x3+bfal2+kfal2,y3,z3], [x3+bfal2+kfal2,y3,kfal], [x3+bfal2+kfal2,kfal,z3], [x3+bfal2+kfal2,kfal,kfal], [x3-bfal2+kfal2,y3,z3], [x3-bfal2+kfal2,y3,kfal], [x3-bfal2+kfal2,kfal,z3], [x3-bfal2+kfal2,kfal,kfal]]
        cloud3 = trimesh.points.PointCloud(poinst3)
        hull_mesh3 = cloud3.convex_hull
        hull_mesh = hull_mesh + hull_mesh3
    
    #Belső falak generálása y mentén
    for i in range(1,ykomponens):
        x3 = x2
        y3 = i*y2/ykomponens
        z3 = bz
        bfal2=bfal/2
        #2 oldalról van fal és ezért még egyszer bele kell számolni, viszont a belső falat is 2x-er kell ezért a felével még tolunk
        kfal2=kfal/2
        poinst3 = [[x3,y3+bfal2+kfal/2,z3], [x3,y3+bfal2+kfal/2,kfal], [x3,y3-bfal2+kfal/2,z3], [x3,y3-bfal2+kfal/2,kfal], [kfal,y3+bfal2+kfal/2,z3], [kfal,y3+bfal2+kfal/2,kfal], [kfal,y3-bfal2+kfal/2,z3], [kfal,y3-bfal2+kfal/2,kfal]]
        cloud3 = trimesh.points.PointCloud(poinst3)
        hull_mesh3 = cloud3.convex_hull
        hull_mesh = hull_mesh + hull_mesh3
    # Exportálás és megnyitás
    hull_mesh.export('output.stl')
    if megnyit:
        try:
            os.startfile('output.stl')
        except Exception:
            hull_mesh.show()
#UI függvények
def program():
    boxgenerator()

#UI beállítása
root = tk.Tk(className="Box generator")

#x érték beállítása
xshow =  tk.Label(root, text="x=",anchor="e")
xshow.grid(row=0, column=0, sticky="e")
xvalue = tk.Entry(root)
xvalue.insert(0, x)
xvalue.grid(row=0, column=1)

#y érték beállítása
yshow =  tk.Label(root, text="y=",anchor="e")
yshow.grid(row=1, column=0, sticky="e")
yvalue = tk.Entry(root)
yvalue.insert(0, y)
yvalue.grid(row=1, column=1)

#z érték beállítása
zshow =  tk.Label(root, text="z=",anchor="e")
zshow.grid(row=2, column=0, sticky="e")
zvalue = tk.Entry(root)
zvalue.insert(0, z)
zvalue.grid(row=2, column=1)

#bz érték beállítása
bzshow =  tk.Label(root, text="Belső falak magassága=",anchor="e")
bzshow.grid(row=3, column=0, sticky="e")
bzvalue = tk.Entry(root)
bzvalue.insert(0, bz)
bzvalue.grid(row=3, column=1)

#y komponensek beállítása
ykomponensshow =  tk.Label(root, text="y komponensek=",anchor="e")
ykomponensshow.grid(row=4, column=0, sticky="e")
ykomponensvalue = tk.Entry(root)
ykomponensvalue.insert(0, ykomponens)
ykomponensvalue.grid(row=4, column=1)

#x komponensek beállítása
xkomponensshow =  tk.Label(root, text="x komponensek=",anchor="e")
xkomponensshow.grid(row=5, column=0, sticky="e")
xkomponensvalue = tk.Entry(root)
xkomponensvalue.insert(0, xkomponens)
xkomponensvalue.grid(row=5, column=1)

#Külső falak vastagságának beállítása
kfalshow =  tk.Label(root, text="Külső falak vastagsága=",anchor="e")
kfalshow.grid(row=6, column=0, sticky="e")
kfalvalue = tk.Entry(root)
kfalvalue.insert(0, kfal)
kfalvalue.grid(row=6, column=1)

#Belső falak vastagságának beállítása
bfalshow =  tk.Label(root, text="Belső falak vastagsága=",anchor="e")
bfalshow.grid(row=7, column=0, sticky="e")
bfalvalue = tk.Entry(root)
bfalvalue.insert(0, bfal)
bfalvalue.grid(row=7, column=1)

#Kerekítés checkbox
kerekites2= tk.BooleanVar()
kerekiteslabel = tk.Label(root, text="Kerekítés:",anchor="e")
kerekiteslabel.grid(row=8, column=0, sticky="e")
kerekites = tk.Checkbutton(root,variable=kerekites2,onvalue=True, offvalue=False,anchor="w")
kerekites.select()
kerekites.grid(row=8, column=1, sticky="w")

#Simaság beállítása
simasagshow =  tk.Label(root, text="Simaság=",anchor="e")
simasagvalue = tk.Entry(root)
simasagvalue.insert(0, simasag)
#Nem írható ki a függvénnyel, mert először igaz lesz, viszont kattintáskor még a változó csere előtt hívódik meg a függvény
simasagshow.grid(row=9, column=0, sticky="e")
simasagvalue.grid(row=9, column=1)
def check_kerekit(*args):
    #A kattintás előtti állapotban meghívódik
    if not kerekites2.get():
        simasagshow.grid(row=9, column=0, sticky="e")
        simasagvalue.grid(row=9, column=1)
    else:
        simasagshow.grid_remove()
        simasagvalue.pack_forget()
        simasagshow.pack_forget()
        simasagvalue.grid_remove()
#"Listener" hozzáadása a kerekítés checkboxhoz
kerekites.bind("<Button-1>", check_kerekit)

#Megnyitás checkbox
megnyit2= tk.BooleanVar()
megnyitaslabel = tk.Label(root, text="Megnyitás:",anchor="e")
megnyitaslabel.grid(row=10, column=0, sticky="e")
megnyitas = tk.Checkbutton(root,variable=megnyit2,onvalue=True, offvalue=False,anchor="w")
megnyitas.select()
megnyitas.grid(row=10, column=1, sticky="w")

#Generálás gomb
button = tk.Button(root, text="Generate!", command=program)
button.grid(row=11, column=0, columnspan=2)

root.mainloop()