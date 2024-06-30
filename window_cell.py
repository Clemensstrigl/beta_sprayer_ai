import math


WALL_VOLUME = 0
JUGS_HORN = 1
CRIMPS = 2
SLOPERS = 3
PINCHES = 4


# Sandpaper (120) = Static Friction Coefficient = 1.152



class Cell:

    def __init__(self, id,roll, pitch, quality=1, matchable=True, percentage=0):
        self.id = id #0= Wall/Volume, 1 = Jugs/Horns, 2 = crimps/pockets/footchips, 3 = slopers, 4 = pinckes, 
        self.roll = roll 
        self.pitch = pitch
        self.quality = quality #potential friction score to more specify how good something is
        self.matchable = matchable #can more than one hand fit on the hold (based on size of actual hold)
        self.percentage = percentage
    


    def to_list(self):
        return [self.id, self.roll, self.pitch, self.quality, self.matchable]



        
    
class Hold():
    
    def __init__(self, id,x,y,radius, grip_loc, quality, type, matchable, pitch_of_wall):
        assert(id >= 0)
        assert(grip_loc != [])
        assert(quality >= 0  and quality <=1)
        assert(type >= 0 and type <= 4) 
        assert(x >= 0 and y >= 0 and radius >= 0)

    

        self.id = id
        self.grip_loc = grip_loc
        self.quality = quality
        self.type = type #0= Wall/Volume, 1 = Jugs/Horns, 2 = crimps/pockets/footchips, 3 = slopers, 4 = pinckes, 
        self.x = x
        self.y = y
        self.radius = radius
        self.matchable = matchable
        self.pitch = pitch_of_wall
    
    def populate_cell(self, x1,y1,x2,y2):
        assert(x1 >= 0 and x2 >= 0 and y1 >= 0 and y2 >=0)
        assert(x2 > x1)
        assert(y2 > y1)
        
        grip_in_cell = False
        max_percentage = 0  
        max_percentage_slope = 0
        for [g_x1,g_y1,g_x2,g_y2] in self.grip_loc:
            intersection_x1 = max(x1, g_x1)
            intersection_y1 = max(y1, g_y1)
            intersection_x2 = min(x2, g_x2)
            intersection_y2 = min(y2, g_y2)

            if intersection_x1 < intersection_x2 and intersection_y1 < intersection_y2:
                intersection_area = (intersection_x2 - intersection_x1) * (intersection_y2 - intersection_y1)
                grip_area = (g_x2 - g_x1) * (g_y2 - g_y1)

                percentage_inside = (intersection_area / grip_area) * 100

                if percentage_inside > max_percentage:
                    max_percentage = percentage_inside
                    max_percentage_slope = (g_y2-g_y1) / (g_x2 - g_x1)
                    grip_in_cell = True

        if grip_in_cell:
            return grip_in_cell, Cell(self.type, self.slope_to_angle(max_percentage_slope), self.pitch, self.quality, self.matchable, max_percentage)
            

        return grip_in_cell, None

    def slope_to_angle(self, slope):
        """
        Converts a given slope to an angle on the unit circle in degrees.
        
        Args:
            slope (float): The slope of the line (rise over run).
        
        Returns:
            float: The angle in degrees.
        """
        # Calculate the angle in radians
        angle_radians = math.atan(slope)
        
        # Convert radians to degrees
        angle_degrees = math.degrees(angle_radians)
        
        # Normalize the angle to be between 0 and 360 degrees
        if angle_degrees < 0:
            angle_degrees += 360
        
        return angle_degrees

































        
                
        




    

