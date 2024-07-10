from window_cell import *
import math, random, os
import tkinter as tk
from tkinter import ttk
from utils import *


class Route_Window():

    def __init__(self, holds, window_height, window_width, window_resolution, x_padding, y_padding, max_height, max_width, window_center_x_start, window_center_y_start, min_hold_grip_area_height):
        

        assert(type(holds) == list)
        assert(holds != [])
        assert(window_height > 0 and window_width > 0)
        assert(int(window_height*100000)%int(window_resolution*100000) == 0)
        assert(int(window_width*100000)% int(window_resolution*100000) == 0)
        assert(window_center_x_start >= 0 and window_center_y_start >= 0)
        assert(x_padding + window_width + window_center_x_start <= max_width)
        assert(y_padding + window_height + window_center_y_start <= max_height)
        assert(max_height >= window_height+y_padding and max_width >= window_width)
        assert(window_center_x_start + window_width/2  <= max_width)
        assert(window_center_y_start + window_height/2  <= max_height)
        assert(window_center_x_start - window_width/2  >= 0 )
        assert(window_center_y_start - window_height/2  >= 0)
        assert(window_resolution > 0)
        assert(min_hold_grip_area_height != None and min_hold_grip_area_height >0)
        

        self.holds = holds
        self.window_height = window_height 
        self.window_width = window_width
        self.window_resolution = window_resolution
        self.x_padding = x_padding
        self.y_padding = y_padding
        self.max_height= max_height
        self.max_width = max_width
        self.window_center_x= window_center_x_start
        self.window_center_y = window_center_y_start
        self.last_hold_added = False
        self.current_holds_in_view = []
        self.left_or_right = True #False = Left, True = Right
        self.up_or_down = True #False = down, True = up
        self.first_in_view_hold_index = -1
        self.min_hold_grip_area_height = min_hold_grip_area_height
        Hold.set_static_value(min_hold_grip_area_height)
        window_row = [ None for _ in range(int(self.window_width/self.window_resolution))]
        self.window = [window_row for _ in range(int(self.window_height/self.window_resolution))]

        self.init_window()


        # Create Tkinter window
        self.root = tk.Tk()
        self.root.geometry("500x500")
        self.root.title("Window Visualization")

    def init_window(self):
        self.window = self.wall_2_window()
        self.current_holds_in_view = self.get_current_holds_in_view()
        self.overlay_holds(self.current_holds_in_view)

    #after initing the window will only wall Cell objects, we will now over lay all holds found to be inside the window area
    #      
    def overlay_holds(self, holds):

        #window start in world coordiantes
        wall_x_start = (self.window_center_x - self.window_width/2)
        wall_y_start = (self.window_center_y - self.window_height/2)

        for hold in holds:
            
            cell_col_start_id = 0
            cell_row_start_id = 0
            cell_col_end_id = int(self.window_width/self.window_resolution)
            cell_row_end_id = int(self.window_height/self.window_resolution)

            #get the area that the holds would populate
            if(hold.x - hold.radius - wall_x_start >= 0):
                cell_col_start_id = int((hold.x - hold.radius - wall_x_start)/ self.window_resolution)

            if(hold.y - hold.radius - wall_y_start >= 0):
                cell_row_start_id = int((hold.y - hold.radius - wall_y_start)/self.window_resolution)

            if(hold.x + hold.radius - wall_x_start <= self.window_width):
                cell_col_end_id = int((hold.x + hold.radius - wall_x_start)/ self.window_resolution)

            if(hold.y + hold.radius - wall_y_start <= self.window_height):
                cell_row_end_id = int((hold.y + hold.radius - wall_y_start)/self.window_resolution)
            
            print(f"Cell IDS: ({cell_row_start_id}, {cell_col_start_id}), ({cell_row_end_id}, {cell_col_end_id})")
            
            
            
            #have to add 1 to ensure that we are getting atleast the singular cell where the full hold is contained within
            for row in range(cell_row_start_id, cell_row_end_id):
                if row > self.window_height//self.window_resolution:
                    print("hit oustide of y window cells")
                    break
                
                for col in range(cell_col_start_id, cell_col_end_id ):
                    
                    if col > self.window_width//self.window_resolution:
                        print("hit outside of x window cell")
                        break

                    #get world coordiantes of window
                    cell_x1 = col * self.window_resolution + wall_x_start
                    cell_x2 = cell_x1 + self.window_resolution
                    
                    cell_y1 = row * self.window_resolution + wall_y_start
                    cell_y2 = cell_y1 + self.window_resolution
                    print(f"Cell LOC: ({cell_x1}, {cell_y1}), ({cell_x2}, {cell_y2})")

                    #get the location and angle of 
                    ret, cell = hold.populate_cell(cell_x1,cell_y1, cell_x2, cell_y2)
                    #if a greater percentage of the grip is held within the cell, populate the cell with that the new cell calulated
                    if ret and self.window[row][col].percentage < cell.percentage:
                        print(f"new cell at: {row}, {col}")
                        self.window[row][col] = cell
            
        

    
    #to be implemented by children of Route_window. 
    # based on the wall config we will want to populate the base wall window differently.
    def wall_2_window(self):
        return self.window

    #loop through list of holds and list all that are currently in view of the window
    def get_current_holds_in_view(self):
        
        current_holds = []
        window_y_start = (self.window_center_y - self.window_height/2) #get the bottom of the window, in world coorodiantes
        window_x_start = (self.window_center_x - self.window_width/2)

        window_y_end = window_y_start + self.window_height
        window_x_end = window_x_start + self.window_width

        self.first_in_view_hold_index = None

        for idx in range(len(self.holds)):
            hold = self.holds[idx]
            #have to check if any part of the hold is contained inside the window, not just the center
            if hold.x-hold.radius >= window_x_start and hold.x+hold.radius <= window_x_end and hold.y-hold.radius >= window_y_start:
                if hold.y+hold.radius <= window_y_end:
                    if self.first_in_view_hold_index == None:
                        print("First hold in view: ", idx)
                        self.first_in_view_hold_index = idx
                    current_holds.append(hold)
                    print(f"{idx}/{len(self.holds)} in view")
                    self.last_hold_added = True
                else:
                    self.last_hold_added = False
                    break
        
        

        return current_holds
                    

        

    #offset center of window and reinit the window
    #potential future upgrade: move all cells by off set and then simply fill in any missing holds and wall bit. 
    #I kept it like this to minimzie code and code errors
    def update_window(self, x_off_set, y_off_set):

        if x_off_set >= 0:  
            #assert( x_off_set + self.window_center_x + self.x_padding + self.window_width/2 <= self.max_width)
            self.left_or_right = True
        else:
            #assert( self.window_center_x - self.window_width/2 + self.x_padding + x_off_set >= 0)
            self.left_or_right = False
        
        if y_off_set >= 0:
            #assert( y_off_set + self.window_center_y + self.y_padding + self.window_height/2 <= self.max_height)
            self.up_or_down = True
        else:
            #assert( self.window_center_y - self.window_height/2 + self.y_padding + y_off_set >= 0)
            self.up_or_down = False


        self.window_center_x = self.window_center_x + x_off_set
        self.window_center_y = self.window_center_y + y_off_set

        self.init_window()

        return self.window

    
    #flatten and return window in sinlge array of all values
    def get_window_flattened(self):
        final = []

        for row in self.window:
            for cell in row:
                final += cell.to_list()
        
        return final

    #flatten what every comes into the function
    def flatten(self, something):
        if isinstance(something, (list, tuple, set, range)):
            for sub in something:
                yield from self.flatten(sub)
        else:
            yield something
    
    #visualize the window on a window
    def visualize(self):
        out_grid = self.window

       
        # Create a frame for the grid
        grid_frame = ttk.Frame(self.root)
        grid_frame.pack(padx=10, pady=10)
        width = int(1/len(out_grid[0]))
        height = int(1/len(out_grid))

        self.root.bind("<Up>", self.on_key_press)
        self.root.bind("<Down>", self.on_key_press)
        self.root.bind("<Left>", self.on_key_press)
        self.root.bind("<Right>", self.on_key_press)

        

        # Create labels for each cell
        for row in range(len(out_grid)):
          print()
          for col in range(len(out_grid[row])):
                print(self.window[row][col].type, end=", ")
                color = "green"
                cell = out_grid[row][col]
                if cell.type != 0:
                    color = "red"
                label = tk.Label(grid_frame, text=str(cell.type), relief="solid", width=width, height=height, bg=color)
                label.grid(row=len(out_grid)-1-row, column=col, padx=2, pady=2)
                
        self.root.mainloop()

        
    
    def on_key_press(self, event):
        """Handle the up and down key presses to modify and redraw the grid."""
        print("key pressed")
        if event.keysym == "Up":
            print("up")
            self.update_window(0,self.window_resolution*2)
        elif event.keysym == "Down":
            print("down")
            self.update_window(0,-self.window_resolution*2)
        elif event.keysym == "Left":
            print("left")
            self.update_window(-self.window_resolution*2, 0)
        elif event.keysym == "Right":
            print("right")
            self.update_window(self.window_resolution*2, 0)
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.visualize()
