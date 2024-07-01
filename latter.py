from route import Route_Window
import math
import random
from window_cell import *



class Latter(Route_Window):

    def __init__(self,hold_type, hold_dist_x, hold_dist_y,hold_height,hold_width,max_random_x_offset, max_random_y_offset,symetric, wall_roll, wall_pitch, window_height, window_width, window_resolution, x_padding, y_padding, max_height, max_width, window_center_x_start, window_center_y_start):
        
        self.hold_type = hold_type
        self.hold_dist_x = hold_dist_x
        self.hold_dist_y = hold_dist_y
        self.symetric = symetric
        self.hold_height = hold_height
        self.hold_width = hold_width 
        self.max_random_x_offset = max_random_x_offset #0 up to this offset can be chosen
        self.max_random_y_offset = max_random_y_offset #0 up to this offset can be chosen
        self.holds = self.generate_holds(0)
        self.cell = Cell(0,wall_roll, wall_pitch)
        super.__init__(self.holds,window_height, window_width, window_resolution, x_padding, y_padding, max_height, max_width, window_center_x_start, window_center_y_start)
    
    
    def init_window(self):
        self.window = self.wall_2_window()
        self.current_holds_in_view = self.get_current_holds_in_view()
        self.window = self.overlay_holds(self.current_holds_in_view)

    def generate_holds(self):

        return

    def wall_2_window(self):

        for row in range(self.window_height/self.window_resolution):
            for col in range(self.window_width/self.window_resolution):
                self.window[row][col] = self.cell

        return
    
    def generate_holds(self, y_start):

        current_holds = []
       
        for y in range(y_start, y_start +1000, self.hold_dist_y):
            curr_x_offset = self.hold_dist_x * 2 *random.random() + self.max_random_x_offset * random.random()
            curr_y_offset = self.max_random_y_offset * random.random()

            if random.random <= self.symetric:
                
                current_holds.append(Hold(self.hold_type, self.window_center_x-curr_x_offset, ))
                curr_x_offset = self.hold_dist_x * 2 *random.random() + self.max_random_x_offset * random.random()
                

        return
        