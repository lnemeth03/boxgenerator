import os
import trimesh
import numpy as np
import tkinter as tk
from tkinter import ttk

#Beállítások
#megnyit =  #Megnyitja-e a generált fájlt
x = 15 #A doboz szélessége
y = 20 #A doboz mélysége
z = 5 #A doboz magassága
ykomponens = 2 #A komponensek száma az y tengely mentén
xkomponens = 1 #A komponensek száma az x tengely mentén
kfal = 0.2 #Külső falak vastagsága
bfal =  0.1 #Belső falak vastagsága
    
# A csak, hogy vscode alatt is ugyanabba a mappába generáljon
os.chdir(os.path.dirname(os.path.abspath(__file__)))
def boxgenerator():
    #Értékek beolvasása
    try:
        x = float(xvalue.get())
        y = float(yvalue.get())
        z = float(zvalue.get())
        ykomponens = int(ykomponensvalue.get())
        xkomponens = int(xkomponensvalue.get())
        kfal = float(kfalvalue.get())
        bfal = float(bfalvalue.get())
        megnyit = megnyit2.get()
    except Exception:
        #Error window
        error=tk.Tk()
        error.title("Error")
        error.geometry("200x50")
        errorlabel = tk.Label(error, text="Hibás argumentumok!")
        errorlabel.pack()
        error.mainloop()
        return
    #Megadott méretű doboz generálása
    points = [[x,y,z], [x,y,0], [x,0,z], [x,0,0], [0,y,z], [0,y,0], [0,0,z], [0,0,0]]
    cloud = trimesh.points.PointCloud(points)
    hull_mesh = cloud.convex_hull

    #Doboz belsejének törlése (külső falak megtartásával)
    x2 = x - kfal
    y2 = y - kfal
    z2 = z #A tetejét el kell érnie a kivágásnak
    poinst2 = [[x2,y2,z2], [x2,y2,kfal], [x2,kfal,z2], [x2,kfal,kfal], [kfal,y2,z2], [kfal,y2,kfal], [kfal,kfal,z2], [kfal,kfal,kfal]]
    cloud2 = trimesh.points.PointCloud(poinst2)
    hull_mesh2 = cloud2.convex_hull
    hull_mesh = hull_mesh.difference(hull_mesh2)
    ###Később kelhet
    #egyesítés
    #hull_mesh = hull_mesh + hull_mesh2

    # Exportálás és megnyitás
    hull_mesh.export('output.stl')
    try:
        if megnyit:
            os.startfile('output.stl')
    except Exception:
        hull_mesh.show()
#UI függvények
def program():
    boxgenerator()

#UI beállítása
root = tk.Tk()

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

#y komponensek beállítása
ykomponensshow =  tk.Label(root, text="y komponensek=",anchor="e")
ykomponensshow.grid(row=3, column=0, sticky="e")
ykomponensvalue = tk.Entry(root)
ykomponensvalue.insert(0, ykomponens)
ykomponensvalue.grid(row=3, column=1)

#x komponensek beállítása
xkomponensshow =  tk.Label(root, text="x komponensek=",anchor="e")
xkomponensshow.grid(row=4, column=0, sticky="e")
xkomponensvalue = tk.Entry(root)
xkomponensvalue.insert(0, xkomponens)
xkomponensvalue.grid(row=4, column=1)

#Külső falak vastagsága beállítása
kfalshow =  tk.Label(root, text="Külső falak vastagsága=",anchor="e")
kfalshow.grid(row=5, column=0, sticky="e")
kfalvalue = tk.Entry(root)
kfalvalue.insert(0, kfal)
kfalvalue.grid(row=5, column=1)

#Belső falak vastagsága beállítása
bfalshow =  tk.Label(root, text="Belső falak vastagsága=",anchor="e")
bfalshow.grid(row=6, column=0, sticky="e")
bfalvalue = tk.Entry(root)
bfalvalue.insert(0, bfal)
bfalvalue.grid(row=6, column=1)

#Megnyitás gomb
megnyit2= tk.BooleanVar()
megnyitas = tk.Checkbutton(root,variable=megnyit2,onvalue=True, offvalue=False,anchor="w")
megnyitas.select()
megnyitas.grid(row=7, column=1, sticky="w")
megnyitaslabel = tk.Label(root, text="Megnyitás:",anchor="e")
megnyitaslabel.grid(row=7, column=0, sticky="e")
#Generálás gomb
button = tk.Button(root, text="Generate!", command=program)
button.grid(row=8, column=0, columnspan=2)

root.mainloop()