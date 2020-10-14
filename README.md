# Dungeon-Gen-Gravity
Python tool that generates a 2-dimensional dungeon based off of a set of pre-defined room dimensions and room counts.

## Problem
The current most popular ways for generating dungeons usually take one of the following approaches:
* Generate random room sizes, connect randomly generated rooms together with hallways.
* Fill in a predefined area with pre-set rooms, randomly connect them together again with hallways.

Either of these approaches requires that you fill the remaining space between rooms with hallways as there is no guarantee of adjacency, or you must use randomly generated room sizes. This is usually not a big issue, but if you want to design a generator that does not produce hallways as well as using pre-determined room sizes, neither of the above approaches satisfies this constraint.

## Approach

This tool takes a different approach that guarantees both **direct adjacency to at least one other room** (which ensures there are no hallways) as well as **all room dimensions are predefined** (meaning we can custom tailer the rooms). This is done with the following methodology

* From a given set of rooms R, randomly place all rooms within a 2-dimensional space such that there is no overlap between rooms. This generates something similar to approach #2 in the above list, minus the hallways.
* Once generated, pick a central x,y co-ordinate and collapse all rooms towards that point. Essentially pull all rooms in the direction of that point. This guarantees that all rooms will end up colliding, guarnateeing adjacency with at least one other room.
* Once adjacency has been guaranteed, use one of the many pathfinding approaches to generate connections between adjacent rooms without making all adjacencys valid connections.

## Procedure (Room Generation)

The following animations were generated using a roomset of [5,5],[10,5],[5,10],[20,20],[25,5] with 50 rooms.

### Generating the initial set

First we generate an initial set of rooms randomly placed around (0,0,10,10) which is our center defined range. The larger the range the more spread out the rooms will be on initialization. As we can see its highly condensed.

![50 Room Initial Dungeon](https://i.imgur.com/TBINBQ1.png)

Next we 'explode' outwards, spreading the rooms out as much as possible.

![50 Room Explode](https://i.imgur.com/rd9WyEE.gif)

Finally, we 'condense' the rooms towards the center. Note that the center does not have to be a part of (0,0,10,10) and could be an entirely different position.

![50 Room Explode](https://i.imgur.com/vf5k4uN.gif)

This creates the final output as seen below.

![50 Room Final](https://i.imgur.com/2GGiI0c.png)
