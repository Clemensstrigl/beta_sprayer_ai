from route import Route_Window
import math
from window_cell import *



class SymetricLatter(Route_Window):

    def __init__(self,hold_dist,hold_height,hold_width, wall_roll, wall_pitch, window_height, window_width, window_resolution, x_padding, y_padding, max_height, max_width, window_center_x_start, window_center_y_start):
        
        self.hold_dist = hold_dist
        self.hold_height = hold_height
        self.hold_width = hold_width 
        self.cell = Cell(0,wall_roll, wall_pitch)
        super.__init__(window_height, window_width, window_resolution, x_padding, y_padding, max_height, max_width, window_center_x_start, window_center_y_start)
    

    def wall_2_window(self):

        for row in range(self.window_height/self.window_resolution):
            for col in range(self.window_width/self.window_resolution):
                self.window[row][col] = self.cell

        return
    
    def get_current_holds_in_view(self, x = 0, y = 0):



        return
        
    def fill_missing_hold_sections(self, x_off_set=0, y_off_set=0):
        return
    
    def fill_missing_wall_sections(self,x_off_set=0, y_off_set=0):
        return 