'''Main dungeon generating file. See README.md for more information.'''

class Dimension:
    """Class that helps represent a dimension size. This is helpful for when we want to check for collisions between other colliders.
    Note that all given dimension variables are integers.

    Args:
        x (int): x-position of the bottom left corner of the dimension
        y (int): y-position of the bottom left corner of the dimension.
        w (int): width of the dimension
        h (int): height of the dimension

    Returns:
        Dimension: Default Dimension constructor
    """
    def __init__(self, x: int, y: int, w: int, h: int):
        self.x, self.y, self.w, self.h = x, y, w, h

    """Returns a boolean value representing if the given dimension D overlaps within a 2-d coordinate plane with ourself

    Args:
        d (Dimension): The given dimension to check overlaps for

    Returns:
        bool: Whether or not an overlap exists
    """
    def overlap(self, d: Dimension):
        pass

class RoomConnection:
    """Class that represents a connection betwee two rooms. Yes this could just be a tuple, but this way we can expand this a little more effectively.

    Args:
        start (int): Unique ID of the starting room.
        end (int): Unique ID of the ending room.

    Returns:

    """
    def __init__(self, start: int, end: int):
        self.start, self.end = start, end

class Room:
    """Main class for representing a room within our dungeon. The primary values it contains is its position and dimensions.

    Args:
        x,y,w,h (int): See dimension documentation as this gets passed directly into a new dimension object.
        id (int): Unique ID for the room.

    Returns:
        Room: Default room constructor
    """
    def __init__(self, id: int, x: int, y: int, w: int, h: int):
        self.id = id
        self.dimension = Dimension(x,y,w,h)
        