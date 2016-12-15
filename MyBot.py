from hlt import *
from networking import *
from random import shuffle

#Get initial information of game
myID, gameMap = getInit()
sendInit("MartenEnPieter")

#Move function describes move of a single unit, given its location
def move(location):
    site = gameMap.getSite(location)
    
    #Shuffle Cardinals to randomize which direction comes first.
    LOCALCARDINALS = CARDINALS
    shuffle(LOCALCARDINALS)
    
    direction = STILL
    minstrength = float("inf")
    interior = True

    
    for d in LOCALCARDINALS:
        neighbour_site = gameMap.getSite(location, d)
        #Check if all neighbours are of the same owner
        if neighbour_site.owner != myID:
            interior = False
            #Always take enemy/neutral neighbour if your strenght is enough.
            if neighbour_site.strength < site.strength and neighbour_site.strength < minstrength:
                minstrength = neighbour_site.strength
                direction = d
    
    #If the location is interior and with strength more than twice the production, move it to closest border
    if interior and site.strength > 2 * site.production:
        closestborder = float("inf")
        #Loop over all directions to find closest border
        for d in CARDINALS:
            if d == NORTH or d == SOUTH:
                size = gameMap.height/2
            else:
                size = gameMap.width/2
            
            #Move Checkpoint until you reach an exterior site or are halfway the field
            checkpoint = gameMap.getLocation(location,d)
            while gameMap.getSite(checkpoint).owner == myID and gameMap.getDistance(checkpoint, location) < size:
                checkpoint = gameMap.getLocation(checkpoint,d)
            
            if gameMap.getDistance(checkpoint, location) < closestborder:
                direction = d
                closestborder = gameMap.getDistance(checkpoint, location)
    
    return Move(location, direction)

#Loops as long as the game lasts.
while True:
    moves = []
    gameMap = getFrame()
    #loops over all positions and performs Move function if location is owned by us.
    for y in range(gameMap.height):
        for x in range(gameMap.width):
            location = Location(x, y)
            if gameMap.getSite(location).owner == myID:
               moves.append(move(location))
    sendFrame(moves)
