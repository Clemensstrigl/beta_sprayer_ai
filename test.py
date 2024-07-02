from latter import Latter
import os
from dotenv import load_dotenv
load_dotenv()

def main():

    latter_climb = Latter(
        hold_type=int(os.getenv("HOLD_TYPE")),
        hold_dist_x=float(os.getenv("HOLD_DIST_X")),
        hold_dist_y=float(os.getenv("HOLD_DIST_Y")),
        hold_radius=float(os.getenv("HOLD_RADIUS")),
        max_random_x_offset=float(os.getenv("MAX_RANDOM_X_OFFSET")),
        max_random_y_offset=float(os.getenv("MAX_RANDOM_Y_OFFSET")),
        symetric=bool(os.getenv("SYMETRIC")),
        prob_hold_on_same_side=float(os.getenv("PROB_HOLD_ON_SAME_SIDE")),
        prob_hold_change_angle=float(os.getenv("PROB_HOLD_CHANGE_ANGLE")),
        max_angle_change=float(os.getenv("MAX_ANGLE_CHANGE")),
        wall_roll=int(os.getenv("WALL_ROLL")),
        wall_pitch=int(os.getenv("WALL_PITCH")),
        window_height=float(os.getenv("WINDOW_HEIGHT")),
        window_width=float(os.getenv("WINDOW_WIDTH")),
        window_resolution=float(os.getenv("WINDOW_RESOLUTION")),
        x_padding=float(os.getenv("X_PADDING")),
        y_padding=float(os.getenv("Y_PADDING")),
        max_height=float(os.getenv("MAX_HEIGHT")),
        max_width=float(os.getenv("MAX_WIDTH")),
        window_center_x_start=float(os.getenv("WINDOW_CENTER_X_START")),
        window_center_y_start=float(os.getenv("WINDOW_CENTER_Y_START"))
    )

    latter_climb.visualize()


    return 0


if __name__ == "__main__":
    main()