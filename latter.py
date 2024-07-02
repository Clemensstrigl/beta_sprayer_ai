from route import Route_Window
import math
import random
from window_cell import *
import numpy as np


class Latter(Route_Window):

    def __init__(self,hold_type, hold_dist_x, hold_dist_y,hold_radius,max_random_x_offset, max_random_y_offset,symetric,prob_hold_on_same_side,prob_hold_change_angle,max_angle_change, wall_roll, wall_pitch, window_height, window_width, window_resolution, x_padding, y_padding, max_height, max_width, window_center_x_start, window_center_y_start):
        
        self.hold_type = hold_type 
        self.hold_dist_x = hold_dist_x#distance away from center of the climb going up 
        self.hold_dist_y = hold_dist_y #distance between holds
        self.symetric = symetric #if set to True then a hold will be placed on both sides of the center of the holds, if False, it will be offset with slight randmonsess
        self.prob_hold_on_same_side = prob_hold_on_same_side
        self.hold_radius = hold_radius
        self.max_random_x_offset = max_random_x_offset #0 up to this offset can be chosen
        self.max_random_y_offset = max_random_y_offset #0 up to this offset can be chosen
        self.route_center_x = window_center_x_start + x_padding*3
        self.prob_hold_change_angle = prob_hold_change_angle
        self.max_angle_change = max_angle_change
        self.holds = self.generate_holds(0)
        self.wall_pitch = wall_pitch
        self.cell = Cell(0,wall_roll, wall_pitch)
        super.__init__(self.holds,window_height, window_width, window_resolution, x_padding, y_padding, max_height, max_width, window_center_x_start, window_center_y_start)
    
    
    def init_window(self):
        self.window = self.wall_2_window()
        self.current_holds_in_view = self.get_current_holds_in_view()
        self.window = self.overlay_holds(self.current_holds_in_view)

        if self.last_hold_added:
            assert(self.first_in_view_hold_index != -1)
            holds_in_view = self.holds[self.first_in_view_hold_index:]
            self.holds = self.generate_holds(self.window_center_y + self.window_height/2)
            self.holds = holds_in_view + self.holds
            self.last_hold_added = False


    def wall_2_window(self):

        for row in range(self.window_height/self.window_resolution):
            for col in range(self.window_width/self.window_resolution):
                self.window[row][col] = self.cell

        return
    
    def generate_holds(self, y_start):

        current_holds = []

        left_right = False #left = False, Right = True

        if random.random() <= 0.5:
            left_right = True
       
        for y in range(y_start, y_start +1000, self.hold_dist_y):
            curr_y_offset = self.max_random_y_offset * random.random()

            current_holds += self.add_holds(self, y, curr_y_offset, left_right)

            if random.random() <= self.prob_hold_on_same_side:
                continue
            
            left_right = not left_right



               
                

        return current_holds
    
    def add_holds(self, y, curr_y_offset, left_right):
        new_holds = []
        
        #add or remove the y offset to either the holds to move them around a bit and not have them be so stationary which will cause overtraining for specific configurations of holds
        
        for _ in range(2):
            if random.random() <= 0.5:
                curr_y_offset = -curr_y_offset
            
            curr_x_offset = self.hold_dist_x * random.random() + self.max_random_x_offset * random.random()
            if not left_right:
                curr_x_offset = -curr_x_offset

            hold_angle = 0
            if random.random() <= self.prob_hold_change_angle:

                angle_padding = random.random() * self.max_angle_change
                if random.random() <= 0.5:
                    angle_padding = -angle_padding

                hold_angle = hold_angle + angle_padding

            hold_center_x = self.route_center_x + curr_x_offset
            hold_center_y =  y + curr_y_offset

            grip_loc = self.generate_grip_loc(hold_center_x, hold_center_y, hold_angle)

            quality = self.generate_quality_score()

            matchable = True


            new_holds.append(Hold(hold_center_x,hold_center_y, self.hold_radius, grip_loc,quality,self.hold_type,matchable, self.wall_pitch ))

            if not self.symetric:
                break
            
            left_right = not left_right
        
        return new_holds
            
    def generate_quality_score(self,):
        if self.hold_type == 1: #Jug
            return 1 - 0.15 * random.random()
        if self.hold_type == 2: #Crimp
            return 0.9 - 0.4*random.random()
        if self.hold_type == 3: #Sloper
            return 0.75 - 0.4 *random.random()
        if self.hold_type == 4: #Footchips
            return 0.45 - 0.35*random.random()
        if self.hold_type == 5: #Pinches
            return 0.85 - 0.3*random.random()
        if self.hold_type == 6: #Pockets
            return 0.6 - 0.25*random.random()



    
    def generate_grip_loc(self, x,y, hold_angle):
        point1 = [x-self.hold_radius , y]
        point2 = [x+self.hold_radius , y]
        if hold_angle != 0:
            point1 = self.rotate_point(tuple(point1), hold_angle, (x,y))
            point2 = self.rotate_point(tuple(point2), hold_angle, (x,y))

        return point1 + point2

    def rotate_point(self,point, angle, center):
        """Rotate a point around a center by a given angle."""
        angle_rad = np.radians(angle)
        x, y = point
        cx, cy = center

        new_x = cx + (x - cx) * np.cos(angle_rad) - (y - cy) * np.sin(angle_rad)
        new_y = cy + (x - cx) * np.sin(angle_rad) + (y - cy) * np.cos(angle_rad)

        return [new_x, new_y]
        

