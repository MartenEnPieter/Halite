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
    
    for d in LOCALCARDINALS:
        neighbour_site = gameMap.getSite(location, d)
        #Always take enemy/neutral neighbour if your strenght is enough.
        if neighbour_site.owner != myID and neighbour_site.strength < site.strength:
            return Move(location, d)
        #Only move otherwise if you are more than twice the strength of current production value
        elif neighbour_site.owner == myID and site.strength > 2 * site.production:
            return Move(location, d)
    return Move(location, STILL)

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
