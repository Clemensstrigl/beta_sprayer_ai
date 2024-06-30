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

        self.cell = Cell(0,wall_roll, wall_pitch)
        super.__init__(window_height, window_width, window_resolution, x_padding, y_padding, max_height, max_width, window_center_x_start, window_center_y_start)
    

    def wall_2_window(self):

        for row in range(self.window_height/self.window_resolution):
            for col in range(self.window_width/self.window_resolution):
                self.window[row][col] = self.cell

        return
    
    def get_current_holds_in_view(self):

        current_holds = []
        window_y_start = (self.window_center_y - self.window_height/2) #get the bottom of the window, in world coorodiantes
        window_y_start = window_y_start + (self.hold_dist_y - (window_y_start % self.hold_dist_y)) #add to the start the offset to the next lication of a hold

        for y in range(window_y_start, window_y_start + self.window_height, self.hold_height):
            curr_x_offset = self.hold_dist_x * 2 *random.random() + self.max_random_x_offset * random.random()
            curr_y_offset = self.max_random_y_offset * random.random()

            if random.random <= self.symetric:
                
                current_holds.append(Hold(self.hold_type, self.window_center_x-curr_x_offset, ))
                curr_x_offset = self.hold_dist_x * 2 *random.random() + self.max_random_x_offset * random.random()





                
        


        return
        
    def fill_missing_hold_sections(self, x_off_set=0, y_off_set=0):
        return
    
    def fill_missing_wall_sections(self,x_off_set=0, y_off_set=0):
        return 