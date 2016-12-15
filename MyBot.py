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

def isBorder(location):
    for d in CARDINALS:
        neighbour_site = gameMap.getSite(location, d)
        #Check if all neighbours are of the same owner
        if neighbour_site.owner != myID:
            return True
    
    return False
    
def moveBorder(location):
    site = gameMap.getSite(location)
    
    #Shuffle Cardinals to randomize which direction comes first.
    LOCALCARDINALS = CARDINALS
    shuffle(LOCALCARDINALS)
    direction = STILL
    minstrength = float("inf")

    for d in LOCALCARDINALS:
        neighbour_site = gameMap.getSite(location, d)
        #Check if all neighbours are of the same owner
        if neighbour_site.owner != myID and neighbour_site.strength < site.strength and neighbour_site.strength < minstrength:
            #Always take enemy/neutral neighbour if your strenght is enough.
                minstrength = neighbour_site.strength
                direction = d
    
    return Move(location, direction)
    
def moveInterior(location):
    site = gameMap.getSite(location)
    direction = STILL
    
    if site.strength > 2 * site.production:
        borderdistance = float("inf")
        for borderloc in border:
            if gameMap.getDistance(location, borderloc) < borderdistance:
                borderdistance = gameMap.getDistance(location, borderloc)
                angle = gameMap.getAngle(location, borderloc)
                if angle < math.pi/4 and angle >= -math.pi/4:
                    direction = EAST
                if angle < 3*math.pi/4 and angle >= math.pi/4:
                    direction = NORTH
                if angle < -3*math.pi/4 or angle >= 3*math.pi/4:
                    direction = WEST
                if angle < -math.pi/4 and angle >= -3*math.pi/4:
                    direction = NORTH
    
    return Move(location, direction)
        
#Loops as long as the game lasts.
while True:
    #f = open('workfile', 'a')
    #f.write('test')
    #f.close()
    moves = []
    gameMap = getFrame()
    interior = []
    border = []
    #loops over all positions and performs Move function if location is owned by us.
    for y in range(gameMap.height):
        for x in range(gameMap.width):
            location = Location(x, y)
            if gameMap.getSite(location).owner == myID:
                if isBorder(location):
                    border.append(location)
                    moves.append(moveBorder(location))
                else:
                    interior.append(location)
    
    for location in interior:
        moves.append(moveInterior(location))
    
    sendFrame(moves)
