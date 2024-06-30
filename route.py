from window_cell import *
import math


class Route_Window():

    def __init__(self, window_height, window_width, window_resolution, x_padding, y_padding, max_height, max_width, window_center_x_start, window_center_y_start):
        
        assert(window_height > 0 and window_width > 0)
        assert(window_height%window_resolution == 0)
        assert(window_width%window_resolution == 0)
        assert(window_center_x_start >= 0 and window_center_y_start >= 0)
        assert(x_padding + window_width + window_center_x_start <= max_width)
        assert(y_padding + window_height + window_center_y_start <= max_height)
        assert(max_height >= window_height+y_padding and max_width >= window_width)
        assert(window_center_x_start + window_width/2  <= max_width)
        assert(window_center_y_start + window_height/2  <= max_height)
        assert(window_center_x_start - window_width/2  >= 0 )
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
        self.wall_2_window()
        self.get_current_holds_in_view(self.window_center_x, self.window_center_y)
        self.overlay_holds(self.current_holds_in_view)

            
    def overlay_holds(self, holds):

        wall_x_start = (self.window_center_x - self.window_width/2)
        wall_y_start = (self.window_center_y - self.window_height/2)

        for hold in holds:

            cell_col_start_id = int(math.log((hold.x - hold.radius - wall_x_start), self.window_resolution))
            cell_row_start_id = int(math.log((hold.y - hold.radius - wall_y_start), self.window_resolution))
            cell_col_end_id = int(math.log((hold.x + hold.radius - wall_x_start), self.window_resolution))
            cell_row_end_id = int(math.log((hold.y + hold.radius - wall_y_start), self.window_resolution))

            for row in range(cell_row_start_id, (cell_row_end_id+1)):
                for col in range(cell_col_start_id, (cell_col_end_id +1)):

                    cell_x1 = col * self.window_resolution + wall_x_start
                    cell_x2 = cell_x1 + self.window_resolution
                    
                    cell_y1 = row * self.window_resolution + wall_y_start
                    cell_y2 = cell_y1 + self.window_resolution

                    ret, cell = hold.populate_cell(cell_x1,cell_y1, cell_x2, cell_y2)
                    if ret and self.window[row,col].percentage > cell.percentage:
                        self.window[row, col] = cell
            
        return

    

    def wall_2_window(self):
        return
    
    def get_current_holds_in_view(self, x = 0, y = 0):
        return
        
    def fill_missing_hold_sections(self, x_off_set=0, y_off_set=0):
        return
    
    def fill_missing_wall_sections(self,x_off_set=0, y_off_set=0):
        return 

    def update_window(self, x_off_set, y_off_set):

        if x_off_set >= 0:  
            assert( x_off_set + self.window_center_x + self.x_padding + self.window_width/2 <= self.max_width)
            self.left_or_right = True
        else:
            assert( self.window_center_x - self.window_width/2 + self.x_padding + x_off_set >= 0)
            self.left_or_right = False
        
        if y_off_set >= 0:
            assert( y_off_set + self.window_center_y + self.y_padding + self.window_height/2 <= self.max_height)
            self.up_or_down = True
        else:
            assert( self.window_center_y - self.window_height/2 + self.y_padding + y_off_set >= 0)
            self.up_or_down = False


        self.shift_window_values(x_off_set, y_off_set)
        self.fill_missing_wall_sections(x_off_set, y_off_set)
        self.fill_missing_hold_sections(x_off_set, y_off_set)
        return self.window

    
 


    def shift_window_values(self, x_off_set, y_off_set):
        newWindow = self.window

        #if we go to the left
        x_range_old = range(0, (self.window_width + x_off_set)//self.window_resolution)
        x_range_new = range(abs(x_off_set)//self.window_resolution, self.window_width//self.window_resolution)

        # if we go down
        y_range_new = range(0, (self.window_center_y + y_off_set)//self.window_resolution)
        y_range_old = range(abs(y_off_set)//self.window_resolution, self.window_height//self.window_resolution)

        
        if self.left_or_right: #if we go to the right
            x_range_new=  range(0, (self.window_width - x_off_set)//self.window_resolution)
            x_range_old = range(abs(x_off_set)//self.window_resolution, self.window_width//self.window_resolution)
       

        if self.up_or_down: #if we go up
            y_range_old = range(0, (self.window_center_y - y_off_set)//self.window_resolution)
            y_range_new = range(abs(y_off_set)//self.window_resolution, self.window_height//self.window_resolution)
        

        for row_old, row_new in y_range_old, y_range_new:
            for col_old, col_new in x_range_old, x_range_new:
                newWindow[row_new][col_new] = self.window[row_old][col_old]
        
        self.window = newWindow
    
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
            
      
