import math


WALL_VOLUME = 0
JUGS_HORN = 1
CRIMPS = 2
SLOPERS = 3
FOOTCHIPS = 4
PINCHES = 5
POCKETS = 6


# Sandpaper (120) = Static Friction Coefficient = 1.152



class Cell:

    def __init__(self, type,roll, pitch, quality=1, matchable=True, percentage=0):
        self.type = type #0= Wall/Volume, 1 = Jugs/Horns, 2 = crimps, 3 = slopers, 4 = footchips, 5 = pinches, 6 = pockets
        self.roll = roll 
        self.pitch = pitch
        self.quality = quality #potential friction score to more specify how good something is
        self.matchable = matchable #can more than one hand fit on the hold (based on size of actual hold)
        self.percentage = percentage
    


    def to_list(self):
        return [self.type, self.roll, self.pitch, self.quality, self.matchable]



        
    
class Hold():
    
    def __init__(self,x,y,radius, grip_loc, quality, type, matchable, pitch_of_wall, allow_under_clings):
        assert(grip_loc != [])
        assert(quality >= 0  and quality <=1)
        assert(type >= 0 and type <= 4) 
        assert(x >= 0 and y >= 0 and radius >= 0)

    

        
        self.grip_loc = grip_loc
        self.quality = quality
        self.type = type #0= Wall/Volume, 1 = Jugs/Horns, 2 = crimps, 3 = slopers, 4 = footchips, 5 = pinches, 6 = pockets
        self.x = x
        self.y = y
        self.radius = radius
        self.matchable = matchable
        self.pitch = pitch_of_wall
        self.allow_under_clings = allow_under_clings

    
    def populate_cell(self, x1,y1,x2,y2):
        assert(x1 >= 0 and x2 >= 0 and y1 >= 0 and y2 >=0)
        assert(x2 > x1)
        assert(y2 > y1)
        
        grip_in_cell = False
        max_percentage = 0  
        max_percentage_slope = 0
        grip_quadrant = 1
        max_percentage_angle = 0

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

                    grip_center_x = g_x1 + (g_x2 - g_x1)/2
                    grip_center_y = g_y1 + (g_y2 - g_y1)/2

                    grip_quadrant = self.get_grip_quadrant(grip_center_x,grip_in_cell, self.x,self.y)


                    max_percentage_slope = (g_y2-g_y1) / (g_x2 - g_x1)
                    max_percentage_angle = self.slope_to_angle(max_percentage_slope)
                    grip_in_cell = True

        if grip_in_cell:
            return grip_in_cell, Cell(self.type,max_percentage_angle , self.pitch, self.quality, self.matchable, max_percentage)
            

        return grip_in_cell, None

    def get_grip_quadrant(self, grip_x, grip_y, hold_x, hold_y):

        if self.type == 6:
            return 1
        

        quadrant = 1
        if grip_x < hold_x:
            if grip_y < hold_y:
                quadrant = 3
            else:
                quadrant = 2
        else:
            if grip_y < hold_y:
                quadrant = 4

        return quadrant

    def slope_to_angle(self, slope, quadrant):
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
        
        if angle_degrees < 0:
            angle_degrees += 180

        if self.allow_under_clings and (quadrant == 3 or quadrant == 4):
            angle_degrees -= 180
        
        return angle_degrees

































        
                
        




    

