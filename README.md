# boxgenerator
Python script to generate boxes (mainly to hold decks of cards, board game components, etc.)
A dimension of the box are x,y,z units(=probably mm)
The inner dimension of the box is x-2thickness,y-2thickness,z-2thickness units(thickness=>"külső falak vastagsága")
The inner walls are "belső falak vastagsága" units wide
"x komponensek" sets the number of parts the x side is going to be divede (unimplemented method)
"y komponensek" sets the number of parts the y side is going to be divede (unimplemented method)
If "megnyitás" is selected the program will open the generated stl
If there is a problem during reading, or the program finds a problem with the parameters an "error window" is going to appear
