from main import *

dg = DungeonGenerator("seed", Dimension2D(0,0,10,10))
rooms = dg.generateDungeon([RoomTemplate(10,10),RoomTemplate(20,20)], 50)
dg.render(rooms)