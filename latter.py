from route import Route
import math

class Latter ():

    def __init__(self,hold_config, wall_angle, window_height, window_width, window_resolution, x_padding, y_padding, max_height, max_width, window_center_x_start, window_center_y_start):
        
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
        
        
        
        
        self.hold_config = hold_config
        self.wall_angle = wall_angle
        self.window_height = window_height 
        self.window_width = window_width
        self.window_resolution = window_resolution
        self.x_padding = x_padding
        self.y_padding = y_padding
        self.max_height= max_height
        self.max_width = max_width
        self.window_center_x_start = window_center_x_start
        self.window_center_y_start = window_center_y_start
        self.last_hold_added = 0

       

        window_row = [ [] for _ in range(self.window_width/self.window_resolution)]
        self.window = [window_row for _ in range(self.window_height/self.window_resolution)]

    def init_window(self):

        window_y_start = self.window_center_y_start - self.window_height/2
        window_x_start = self.window_center_x_start - self.window_width/2
        window_y_end = self.window_center_y_start + self.window_height/2
        window_x_end = self.window_center_x_start + self.window_width/2

        holds_in_view = []

        for hold_index in range( len(self.hold_config) ):
            if self.hold_config[hold_index].x >= window_x_start and self.hold_config[hold_index].x <= window_x_end and self.hold_config[hold_index].y >= window_y_start:
                    if self.hold_config[hold_index].y <= window_y_end:
                        holds_in_view.append(self.hold_config[hold_index])
                    else:
                        break




            
        for rI, row in enumerate(self.window):
            for cI, cell in enumerate(row):
                cell_x_start = rI * self.window_resolution
                cell_y_start = cI * self.window_resolution
                

    def update_window(self, x_off_set, y_off_set):

        newWindow = self.window
        left_or_right = False #left = True, right = False
        up_or_down = False #up = True, down = False

        x_range = range(abs(x_off_set), self.window_width)
        y_range = range(abs(y_off_set), self.window_height)

        if(x_off_set < 0):
            left_or_right = True
            x_range = range(0, self.window_width + x_off_set)
            
        if(y_off_set < 0):
            up_or_down = True
            y_range = range(0, self.window_height + y_off_set)
        

        for row in y_range:
            for col in x_range:
                newWindow[row][col] = self.window[row]

    def get_window_flattened(self):
        return self.window

        
      

        
    
































        
                
        