import os
from types import ClassMethodDescriptorType
import trimesh
import numpy as np

#Beállítások
megnyit = True #Megnyitja-e a generált fájlt
x = 2 #A doboz szélessége
y = 4 #A doboz mélysége
z = 1 #A doboz magassága

# A csak, hogy vscode alatt is megadott helyen generáljon
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#Pontok felvétele az alap dobozhoz
points = ([x,y,z], [x,y,0], [x,0,z], [x,0,0], [0,y,z], [0,y,0], [0,0,z], [0,0,0])

cloud = trimesh.points.PointCloud(points)
hull_mesh = cloud.convex_hull

###Később kelhet
#kivonás
#hull_mesh = hull_mesh.difference(hull_mesh2)
#egyesítés
#hull_mesh = hull_mesh + hull_mesh2

# Exportálás és megnyitás
hull_mesh.export('output.stl')
#Végeredmény megtekintése
try:
    if megnyit:
        os.startfile('output.stl')
except:
    hull_mesh.show()