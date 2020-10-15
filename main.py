import random 
from PIL import Image, ImageDraw
from typing import List

"""Main dungeon generating file. See README.md for more information."""

class Dimension2D:

    """Class that helps represent a dimension size. This is helpful for when we want to check for collisions between other colliders.
    Note that all given dimension variables are integers.

    Args:
        x (int): x-position of the bottom left corner of the dimension.
        y (int): y-position of the bottom left corner of the dimension.
        w (int): width of the dimension.
        h (int): height of the dimension.

    Returns:
        Dimension: Default Dimension constructor.
    """
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x, self.y, self.width, self.height = x, y, width, height

        """Overlap adjust is a variable that lets us add boundaries to the overlap function. This allows us to add 'buffer'"""
        self.overlapAdjust = 0

    """Returns a boolean value representing if the given dimension D overlaps within a 2-d coordinate plane with ourself.

    Args:
        d (Dimension): The given dimension to check overlaps for.

    Returns:
        bool: Whether or not an overlap exists.
    """
    def overlap(self, d):
        dx = min(self.x + self.width - self.overlapAdjust, d.x + d.width + self.overlapAdjust) - max(self.x - self.overlapAdjust, d.x + self.overlapAdjust)
        dy = min(self.y + self.height - self.overlapAdjust, d.y + d.height + self.overlapAdjust) - max(self.y - self.overlapAdjust, d.y + self.overlapAdjust)
        if dx >= 0 and dy >= 0:
            return dx*dy > 0
        return False

    """Moves the entire room in a given direction. Wrapper for modifying the (x,y) member variables.

    Args:
        x (int): Value to adjust x by.
        y (int): Value to adjust y by.

    Returns:
        None: Simply makes adjustment to member variables.
    """
    def move(self, x: int, y: int):
        self.x, self.y = self.x + x, self.y + y

    """Generates string for position.

    """
    def __str__(self):
        return str(self.x)+","+str(self.y)+","+str(self.width)+","+str(self.height)

class RoomConnection:
    """Class that represents a connection betwee two rooms. Yes this could just be a tuple, but this way we can expand this a little more effectively.

    Args:
        start (int): Unique ID of the starting room.
        end (int): Unique ID of the ending room.

    Returns:

    """
    def __init__(self, start: int, end: int):
        self.start, self.end = start, end

class RoomTemplate:
    """Template of a room; holds only the width and height

    Args:
        w (int): Width
        h (int): Height

    Return:
        RoomTemplate: Default RoomTemplate constructor
    """
    def __init__(self, width, height):
        self.width, self.height = width, height

class Room:
    """Main class for representing a room within our dungeon. The primary values it contains is its position and dimensions.

    Args:
        x,y,w,h (int): See dimension documentation as this gets passed directly into a new dimension object.
        id (int): Unique ID for the room.

    Returns:
        Room: Default room constructor.
    """
    def __init__(self, id: int, x: int, y: int, w: int, h: int):
        self.id = id
        self.dimension = Dimension2D(x,y,w,h)

        self.fill = (random.randint(0,255),random.randint(0,255),random.randint(0,255))

class DungeonGenerator:
    """Main class for generating our dungeon.

    Args:
        seed (string): Seed used to generate the dungeon.
        genDimensions (Dimension2D): Dimensions used as the range to select from when generating a new rooms positions.


    Returns:
        DungeonGenerator: Default DungeonGenerator constructor.
    """
    def __init__(self, seed: str, genDimensions: Dimension2D):
        self.genDimensions, self.seed = genDimensions, seed
        random.seed(seed)


    """Function for generating a random x and y co-ordinate within our defined range.

    Args:
        None: Function uses data from self to run.

    Returns:
        x (int): x position.
        y (int): y position.
    """
    def generateRandomStartingPosition(self) -> (int, int):
        return (int(random.randint(self.genDimensions.x, self.genDimensions.x + self.genDimensions.width)), int(random.randint(self.genDimensions.y, self.genDimensions.y + self.genDimensions.height)))

    """Funcion that will continue to 'shift' rooms until there are no more overlaps

    Args:
        roomDict (dict<int, Room>): Dictionary of rooms by id

    Returns:
        None: Modifying the roomDict directly
    """
    def shiftRoomsRemoveOverlap(self, roomDict: dict):
        roomMod = max(len(roomDict), 50)
        totalRenderCount = 0
        while True:
            self.render(roomDict,outputFile="./output/output_explode_"+str(totalRenderCount)+".png")
            totalRenderCount += 1
            c = 0
            doesOverlap = False
            for roomId in roomDict:
                room = roomDict[roomId]
                roomDim = room.dimension
                for roomOtherId in roomDict:
                    if roomOtherId == roomId:
                        continue
                    if roomDict[roomOtherId].dimension.overlap(roomDim):
                        # Picking a direction and moving it until we now longer have an overlap
                        moveDir = (random.randint(-roomMod,roomMod),random.randint(-roomMod,roomMod))
                        oppositeMoveDir = (-moveDir[0], - moveDir[1])
                        roomDim.move(moveDir[0],moveDir[1])
                        roomDict[roomOtherId].dimension.move(oppositeMoveDir[0], oppositeMoveDir[1])
                        doesOverlap = True
                        c += 1
                        break
            print(c,roomMod)
            if roomMod > 20:
                roomMod -= 1
            if not doesOverlap:
                break
            

    """Dungeon generating function.

    Args:
        rooms (List[RoomTemplate]): List of all possible rooms to pick from.
        roomCount (int): Total number of rooms to generate.

    Returns:
        List[Room]: List of all rooms within the dungeon.
        Room: Starting room within the dungeon
    """
    def generateDungeon(self, rooms: List[RoomTemplate], roomCount: int):
        # Creating a dictionary of unique IDs mapping to the room
        roomDict = {}

        # Generating roomCount # of rooms
        for i in range(roomCount):
            # Getting a template to use for the room (essentially just a tuple wrapper)
            selectedRoomTemplate = random.choice(rooms)

            # Generating a new X and Y for the room to start at. Important to note that this is unlikely to be permanent.
            (newX, newY) = self.generateRandomStartingPosition()

            newRoom = Room(i, newX, newY, selectedRoomTemplate.width,selectedRoomTemplate.height)

            # Putting it into the dictionary
            roomDict[i] = newRoom

        # Checking for overlaps first and shaking everything around until we establish a non-overlap position

        self.shiftRoomsRemoveOverlap(roomDict)

        # Selecting a central point to pull towards
        self.centerX, self.centerY = self.generateRandomStartingPosition()

        # Pivoting all rooms towards the central position

        # Collide dictionary; helps us from re-calculating previously known collides
        collideDictionaryX = {}
        collideDictionaryY = {}

        # Tracking previous movements to ensure we don't do the same thing many times
        movementDictionary = {}

        totalRenderCount = 0
        while True:
            totalCollide = 0
            self.render(roomDict,outputFile="./output/output_condense_"+str(totalRenderCount)+".png")
            totalRenderCount += 1

            for roomId in roomDict:
                room = roomDict[roomId]
                roomDim = room.dimension

                # Calculating the central position of the roomDim
                roomCenterX, roomCenterY = (roomDim.x + (roomDim.width // 2)), (roomDim.y + (roomDim.height // 2))

                # Calculating the move direction (x,y)
                adjustX, adjustY = 1 * (1 if (self.centerX - roomCenterX) > 0 else -1), 1 * (1 if (self.centerY - roomCenterY) > 0 else -1)
                
                # Attempting to make this move
                moveFull = Dimension2D(roomDim.x + adjustX, roomDim.y + adjustY, roomDim.width, roomDim.height)
                moveX = Dimension2D(roomDim.x + adjustX, roomDim.y, roomDim.width, roomDim.height)
                moveY = Dimension2D(roomDim.x, roomDim.y + adjustY, roomDim.width, roomDim.height)

                collide = False

                for otherRoomId in roomDict:
                    # Wait; do we have valid entries within the collide dictionary?
                    # If we do; don't bother we already know we're screwed
                    if roomId in collideDictionaryX and roomId in collideDictionaryY:
                        #print("Skipping based on previous collide " + str(roomId))
                        collide = True
                        totalCollide += 1
                        break

                    if otherRoomId == roomId:
                        continue

                    if moveY and moveY.overlap(roomDict[otherRoomId].dimension):
                        collideDictionaryY[roomId] = otherRoomId
                        moveY = None

                    if moveX and moveX.overlap(roomDict[otherRoomId].dimension):
                        collideDictionaryX[roomId] = otherRoomId
                        moveX = None

                    if not moveX and not moveY:
                        collide = True
                        totalCollide += 1
                        break

                if not collide:
                    newRoomDimension = (moveFull if moveX and moveY else ((moveX if moveX else moveY)))
                    room.dimension = newRoomDimension

                    if roomId not in movementDictionary:
                        movementDictionary[roomId] = set()

                    if str(newRoomDimension) in movementDictionary[roomId]:
                        # This counts as a collision
                        collide = True
                        totalCollide += 1
                        continue

                    else:
                        movementDictionary[roomId].add(str(newRoomDimension))

                    # Removing this room id from everyone who thinks they can't move through me
                    for fixRoomId in roomDict:
                        if fixRoomId in collideDictionaryX and roomId == collideDictionaryX[fixRoomId]:
                            del collideDictionaryX[fixRoomId]
                        if fixRoomId in collideDictionaryY and roomId == collideDictionaryY[fixRoomId]:
                            del collideDictionaryY[fixRoomId]

            print(totalCollide)
            if totalCollide == len(roomDict):
                break

        return roomDict

    """Render function. Takes all of the rooms and outputs them to the provided output file as a png.

    Args:
        rooms (List[Room]): List of all the rooms to save to the output png
        outputFile (str): Filepath (relative or absolute) of the output saved file. Defaults to output.png in the output directory.
    """
    def render(self, rooms: List[Room], outputFile="./output/output.png"):
        im = Image.new("RGB", (300, 300), "white")
        draw = ImageDraw.Draw(im)
        for roomId in rooms:
            room = rooms[roomId]
            roomDim = room.dimension
            draw.rectangle((roomDim.x + 150, roomDim.y + 150, roomDim.x+roomDim.width - 1 + 150, roomDim.y+roomDim.height - 1 + 150), fill=room.fill)
            roomCenterX, roomCenterY = (roomDim.x + (roomDim.width // 2)), (roomDim.y + (roomDim.height // 2))
            #draw.text([roomCenterX, roomCenterY], str(roomId))

        im.save(outputFile)
