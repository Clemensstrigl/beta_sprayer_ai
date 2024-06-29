
WALL_VOLUME = 0
JUGS_HORN = 1
CRIMPS = 2
SLOPERS = 3
PINCHES = 4


# Sandpaper (120) = Static Friction Coefficient = 1.152




class Cell:

    def __init__(self, id,roll, pitch, quality, matchable):
        self.id = id #0= Wall/Volume, 1 = Jugs/Horns, 2 = crimps/pockets/footchips, 3 = slopers, 4 = pinckes, 
        self.roll = roll 
        self.pitch = pitch
        self.quality = quality #potential friction score to more specify how good something is
        self.matchable = matchable #can more than one hand fit on the hold (based on size of actual hold)
    
    def to_list(self):
        return [self.id, self.roll, self.pitch, self.quality, self.matchable]


