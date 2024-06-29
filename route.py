from window_cell import *
import math


class Route_Window():



    def __init__(self, window_height, window_width, window_resolution, x_padding, y_padding, max_height, max_width, window_center_x_start, window_center_y_start):
        
        assert(window_height > 0 and window_width > 0)
        assert(window_center_x_start >= 0 and window_center_y_start >= 0)
        assert(x_padding >= 0 and x_padding + window_width/2 <= max_width)
        assert(y_padding >= 0 and y_padding + window_height/2 <= max_height)
        assert(max_height >= window_height+y_padding and max_width >= window_width)
        assert(window_center_x_start + window_width/2  <= max_width)
        assert(window_center_y_start + window_height/2  <= max_height)
        assert(window_center_x_start - window_width/2  >=0 )
        assert(window_center_y_start - window_height/2  >= 0)
        assert(window_resolution > 0)
        
        
        
        
        self.window_height = window_height 
        self.window_width = window_width
        self.window_resolution = window_resolution
        self.x_padding = x_padding
        self.y_padding = y_padding
        self.max_height= max_height
        self.max_width = max_width
        self.window_center_x= window_center_x_start
        self.window_center_y = window_center_y_start
        self.last_hold_added = 0
        self.current_holds_in_view = []
        self.left_or_right = True #False = Left, True = Right
        self.up_or_down = True #False = down, True = up

        window_row = [ None for _ in range(self.window_width/self.window_resolution)]
        self.window = [window_row for _ in range(self.window_height/self.window_resolution)]

    def init_window(self):

        self.wall_2_Matrix()
        self.get_holds_in_view(self.window_center_x, self.window_center_y)
        self.overlay_holds()

            
    def overlay_holds(self):
        assert(self.current_holds_in_view != [])

        for hold in self.current_holds_in_view:
            self.insert_hold_into_window(hold)

        return

    def insert_hold_into_window(self, hold):
        return


    def wall_2_Matrix(self):
        return
    
    def get_holds_in_view(self, x, y):
        return
        
             

    def update_window(self, x_off_set, y_off_set):
        if x_off_set >= 0:  
            assert( x_off_set + self.window_center_x + self.window_width/2 <= self.max_width)
            self.left_or_right = True
        else:
            assert( self.window_center_x - self.window_width/2 - x_off_set >= 0)
            self.left_or_right = False
        
        if y_off_set >= 0:
            assert( y_off_set + self.window_center_y + self.window_height/2 <= self.max_height)
            self.up_or_down = True
        else:
            assert( self.window_center_y - self.window_height/2 - y_off_set >= 0)
            self.up_or_down = False



        self.shift_window_values(x_off_set, y_off_set)
        self.fill_missing_wall_sections(x_off_set, y_off_set)
        self.fill_missing_hold_sections(x_off_set, y_off_set)
        return self.window

    
    def fill_missing_hold_sections(self, x_off_set, y_off_set):
        return
    
    def fill_missing_wall_sections(self,x_off_set, y_off_set):
        return


    def shift_window_values(self, x_off_set, y_off_set):
        newWindow = self.window
        
        x_range_old = range(0, self.window_width + x_off_set)
        x_range_new = range(abs(x_off_set), self.window_width)

        y_range_old = range(0, (self.window_center_y + y_off_set)/self.window_resolution)
        y_range_new = range(abs(y_off_set), self.window_height)

        if(self.left_or_right):
            x_range_old = range(abs(x_off_set), self.window_width)
            
        if(self.up_or_down):
            y_range_old = range(abs(y_off_set), self.window_height)


        for row in y_range_old:
            for col in x_range_old:
                newWindow[row][col] = self.window[row]

    
    def get_window_flattened(self):
        final = []

        for row in self.window:
            for cell in row:
                final.append(cell.to_list())
        
        return self.flatten(final)

    def flatten(self, something):
        if isinstance(something, (list, tuple, set, range)):
            for sub in something:
                yield from self.flatten(sub)
        else:
            yield something
            
      

        
    
class Hold:
    
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
            return grip_in_cell, Cell(self.type, self.slope_to_angle(max_percentage_slope), self.pitch, self.quality, self.matchable)
            

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

































        
                
        




    

