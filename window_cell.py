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
        self.roll = roll #degree of roll of the hold, between -180 and 180
        self.pitch = pitch #pitch of the wall on which the hold is on 0 - 360
        self.quality = quality #potential friction score to more specify how good a hold is is
        self.matchable = matchable #can more than one hand fit on the hold (based on size of actual hold)
        self.percentage = percentage #the cell coverage percentage of the object within the cell
    
    def to_list(self):
        """
        Returns a list representation of the object .
        """
        return [self.type, self.roll,self.pitch,   self.quality,  self.matchable,self.percentage]  

    def to_json(self):
        """
        Returns a dictionary representation of the object .
        """
        return {
            "type": self.type,  # 0= Wall/Volume, 1 = Jugs/Horns, 2 = crimps, 3 = slopers, 4 = footchips, 5 = pinches, 6 = pockets
            "roll": self.roll,  # degree of roll of the hold, between -180 and 180
            "pitch": self.pitch,  # pitch of the wall on which the hold is on 0 - 360
            "quality": self.quality,  # potential friction score to more specify how good a hold is is
            "matchable": self.matchable,  # can more than one hand fit on the hold (based on size of actual hold)
            "percentage": self.percentage  # the cell coverage percentage of the object within the cell
        }
    def __str__(self):
        """
        Returns a string representation of the Cell object for printing.
        """
        return f"Type: {self.type}, Roll: {self.roll}, Pitch: {self.pitch}, Quality: {self.quality}, Matchable: {self.matchable}, Percentage: {self.percentage}"


        
    
class Hold():
    
    def __init__(self, type,x,y,radius, grip_loc, quality, matchable, pitch_of_wall, allow_under_clings):
        assert(grip_loc != [])
        assert(quality >= 0  and quality <=1)
        assert(x >= 0 and y >= 0 and radius > 0)

        
    

        
        self.grip_loc = grip_loc
        self.quality = quality
        self.type = type #0= Wall/Volume, 1 = Jugs/Horns, 2 = crimps, 3 = slopers, 4 = footchips, 5 = pinches, 6 = pockets
        self.x = x
        self.y = y
        self.radius = radius
        self.matchable = matchable
        self.pitch = pitch_of_wall
        self.allow_under_clings = allow_under_clings

    def to_json(self):
        """
        Returns a dictionary representation of the object suitable for JSON serialization.
        """
        return {
            "type": self.type,  # 0= Wall/Volume, 1 = Jugs/Horns, 2 = crimps, 3 = slopers, 4 = footchips, 5 = pinches, 6 = pockets
            "roll": self.grip_loc,  # degree of roll of the hold, between -180 and 180
            "pitch": self.pitch,  # pitch of the wall on which the hold is on 0 - 360
            "quality": self.quality,  # potential friction score to more specify how good a hold is is
            "matchable": self.matchable,  # can more than one hand fit on the hold (based on size of actual hold)
        }
    def __str__(self):
        """
        Returns a string representation of the Cell object for printing.
        """
        return f"Type: {self.type}, Roll: {self.grip_loc}, Pitch: {self.pitch}, Quality: {self.quality}, Matchable: {self.matchable}"

    
    def populate_cell(self, x1,y1,x2,y2):
        assert(x1 >= 0 and x2 >= 0 and y1 >= 0 and y2 >=0)
        assert(x2 > x1)
        assert(y2 > y1)
        
        grip_in_cell = False
        max_percentage = 0  
        max_percentage_slope = 0
        grip_quadrant = 1
        max_percentage_angle = 0

        for loc in self.grip_loc:
            g_x1 = loc[0]
            g_y1 = loc[1]
            g_x2 = loc[2]
            g_y2 = loc[3]
            intersect, area, percentage = self.do_line_rectangle_intersect(x1, y1, x2, y2,
                                                     g_x1, g_y1, g_x2, g_y2)

            if intersect:
                print("Intersection")

                if percentage > max_percentage:
                    print(f"current percentage: {percentage}")
                    max_percentage = percentage

                    grip_center_x = g_x1 + (g_x2 - g_x1)/2
                    grip_center_y = g_y1 + (g_y2 - g_y1)/2

                    grip_quadrant = self.get_grip_quadrant(grip_center_x,grip_center_y, self.x,self.y)
                    print(f"quadrant: ${grip_quadrant}")

                    max_percentage_slope = (g_y2-g_y1) / (g_x2 - g_x1)
                    max_percentage_angle = self.slope_to_angle(max_percentage_slope, grip_quadrant)
                    grip_in_cell = True
                else:
                    print(f"current percentage: {percentage}")
            else: 
                print("no Intersection")

        if grip_in_cell:
            return grip_in_cell, Cell(self.type,max_percentage_angle , self.pitch, self.quality, self.matchable, max_percentage)
            

        return grip_in_cell, None
    def do_line_rectangle_intersect(self,rect_corner1_x, rect_corner1_y, rect_corner2_x, rect_corner2_y,
                                line_start_x, line_start_y, line_end_x, line_end_y):
        """
        Calculates if a line intersects a rectangle, returns the length of intersection, and the 
        percentage of the rectangle's area covered by the line.
        Args:
            rect_corner1_x: x-coordinate of the first corner of the rectangle.
            rect_corner1_y: y-coordinate of the first corner of the rectangle.
            rect_corner2_x: x-coordinate of the second corner of the rectangle.
            rect_corner2_y: y-coordinate of the second corner of the rectangle.
            line_start_x: x-coordinate of the start point of the line.
            line_start_y: y-coordinate of the start point of the line.
            line_end_x: x-coordinate of the end point of the line.
            line_end_y: y-coordinate of the end point of the line.
        Returns:
            A tuple:
            - True if the line intersects the rectangle, False otherwise.
            - The length of intersection if they intersect, 0 otherwise.
            - The percentage of the rectangle's area covered by the line if they intersect, 0 otherwise.
        """
        # Calculate the coordinates of the opposite corners for the rectangle
        rect_corner2_x = max(rect_corner1_x, rect_corner2_x)
        rect_corner2_y = max(rect_corner1_y, rect_corner2_y)
        # Print the xy locations of the rectangle and line
        print(f"Rectangle: ({rect_corner1_x}, {rect_corner1_y}), ({rect_corner2_x}, {rect_corner2_y})")
        print(f"Line: ({line_start_x}, {line_start_y}), ({line_end_x}, {line_end_y})")
        # Calculate the line's slope and y-intercept
        if line_end_x - line_start_x != 0:
            slope = (line_end_y - line_start_y) / (line_end_x - line_start_x)
            y_intercept = line_start_y - slope * line_start_x
        else:
            slope = float('inf')
            y_intercept = None
        # Define the rectangle's sides as lines
        rect_sides = [
            ((rect_corner1_x, rect_corner1_y), (rect_corner2_x, rect_corner1_y)),  # Top side
            ((rect_corner2_x, rect_corner1_y), (rect_corner2_x, rect_corner2_y)),  # Right side
            ((rect_corner2_x, rect_corner2_y), (rect_corner1_x, rect_corner2_y)),  # Bottom side
            ((rect_corner1_x, rect_corner2_y), (rect_corner1_x, rect_corner1_y)),  # Left side
        ]
        # Check for intersection with each side of the rectangle
        intersection_points = []
        for side_start, side_end in rect_sides:
            intersection_point = self.calculate_line_intersection(line_start_x, line_start_y, line_end_x, line_end_y,
                                                            side_start[0], side_start[1], side_end[0], side_end[1])
            if intersection_point:
                intersection_points.append(intersection_point)
        # Calculate the length of intersection and percentage of coverage
        intersection_length = 0
        if intersection_points:
            intersection_length = self.calculate_distance(intersection_points[0][0], intersection_points[0][1],
                                                    intersection_points[-1][0], intersection_points[-1][1])
            rect_area = (rect_corner2_x - rect_corner1_x) * (rect_corner2_y - rect_corner1_y)
            percentage_covered = (intersection_length / rect_area) * 100
        return bool(intersection_points), intersection_length, percentage_covered
    
    def calculate_line_intersection(self,line1_start_x, line1_start_y, line1_end_x, line1_end_y,
                                        line2_start_x, line2_start_y, line2_end_x, line2_end_y):
        """
        Calculates the intersection point of two lines.
        Args:
            line1_start_x: x-coordinate of the start point of the first line.
            line1_start_y: y-coordinate of the start point of the first line.
            line1_end_x: x-coordinate of the end point of the first line.
            line1_end_y: y-coordinate of the end point of the first line.
            line2_start_x: x-coordinate of the start point of the second line.
            line2_start_y: y-coordinate of the start point of the second line.
            line2_end_x: x-coordinate of the end point of the second line.
            line2_end_y: y-coordinate of the end point of the second line.
        Returns:
            The intersection point as a tuple (x, y), or None if the lines are parallel or coincide.
        """
        # Calculate slopes and y-intercepts
        if line1_end_x - line1_start_x != 0:
            slope1 = (line1_end_y - line1_start_y) / (line1_end_x - line1_start_x)
            y_intercept1 = line1_start_y - slope1 * line1_start_x
        else:
            slope1 = float('inf')
            y_intercept1 = None
        if line2_end_x - line2_start_x != 0:
            slope2 = (line2_end_y - line2_start_y) / (line2_end_x - line2_start_x)
            y_intercept2 = line2_start_y - slope2 * line2_start_x
        else:
            slope2 = float('inf')
            y_intercept2 = None
        # Check for parallel or coincident lines
        if slope1 == slope2:
            return None  # Lines are parallel or coincide
        # Calculate intersection point
        if slope1 == float('inf'):
            x = line1_start_x
            y = slope2 * x + y_intercept2
        elif slope2 == float('inf'):
            x = line2_start_x
            y = slope1 * x + y_intercept1
        else:
            x = (y_intercept2 - y_intercept1) / (slope1 - slope2)
            y = slope1 * x + y_intercept1
        return (x, y)
    def calculate_distance(self,x1, y1, x2, y2):
        """
        Calculates the distance between two points.
        Args:
            x1: x-coordinate of the first point.
            y1: y-coordinate of the first point.
            x2: x-coordinate of the second point.
            y2: y-coordinate of the second point.
        Returns:
            The distance between the two points.
        """
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


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

































        
                
        




    

