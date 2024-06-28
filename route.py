
class Route():

    def __init__(self,hold_config, wall_config, wall_resolution, window_height, window_width, window_resolution, head_padding, max_height, max_width, window_x_start, window_y_start):
        self.hold_config = hold_config #list of lists where each index is a config value
        self.wall_config = wall_config #Wall 
        self.wall_resolution = wall_resolution
        self.window_height = window_height #height  of window in centimeters
        self.window_width = window_width # width of window in centimeters
        self.window_resolution = window_resolution #how many centimeters per window cell
        self.head_padding = head_padding #padding above the center of mass passed in and the center of frame
        self.max_height = max_height
        self.max_width = max_width
        self.window_x_start = window_x_start
        self.window_y_start = window_y_start

        assert(self.window_resolution > 0)

    
    def get_window_at_start(self, xOffset, yOffset):

        if xOffset > self.max_width or yOffset > self.max_height:
            return False, {}
        if xOffset < 0 or yOffset < 0:
            return False, {}
        window_row = [ [] for _ in range(self.window_width/self.window_resolution)]
        window = [window_row for _ in range(self.window_height/self.window_resolution)]
        
        for row in window:
            for cell in row:
                continue





        
        




    

