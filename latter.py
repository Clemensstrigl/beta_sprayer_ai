from route import Route_Window
import math
from window_cell import *



class Latter(Route_Window):

    def __init__(self,hold_config, wall_angle, window_height, window_width, window_resolution, x_padding, y_padding, max_height, max_width, window_center_x_start, window_center_y_start):
        
        
        
        
        
        
        self.hold_config = hold_config
        self.wall_angle = wall_angle
        
        super.__init__(window_height, window_width, window_resolution, x_padding, y_padding, max_height, max_width, window_center_x_start, window_center_y_start):
        

    def init_window(self):

        

        self.wall_2_Matrix()
        self.overlay_holds()

            
    def overlay_holds(self):
        return


    def wall_2_Matrix(self,):

        for rI, row in enumerate(self.window):
            for cI, cell in enumerate(row):
                self.window[rI][cI] = Cell(WALL_VOLUME, self.roll, self.pitch, self.wall_quality)

    def get_holds_in_view(self, x, y):

        assert(x >= 0 and x <= self.max_width)
        assert(y >= 0 and y <= self.max_height)

        window_y_start = y - self.window_height/2
        window_x_start = x - self.window_width/2
        window_y_end = y + self.window_height/2
        window_x_end = x + self.window_width/2

        holds_in_view = []

        for hold_index in range( len(self.hold_config) ):
            if self.hold_config[hold_index].x >= window_x_start and self.hold_config[hold_index].x <= window_x_end and self.hold_config[hold_index].y >= window_y_start:
                    if self.hold_config[hold_index].y <= window_y_end:
                        holds_in_view.append(self.hold_config[hold_index])
                    else:
                        break
        
        self.current_holds_in_view = holds_in_view
        return
        
             

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

        
      

        
    
































        
                
        