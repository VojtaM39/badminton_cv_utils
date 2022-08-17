from utils.player_position_calculator import get_transformation_matrix, get_warped_court_corners, warp_point, get_player_type, get_middle_of_warped_court
from utils.corner_detector import detect_corners
import cv2
import numpy as np

IMAGE_PATH="./tmp/image1.png"

PLAYERS = [(953, 588), (709, 937), (713, 449), (52, 669), (1571, 700)]
WARPED_COURT_DIM = (305, 670)
WARPED_COURT_DIM_OFFSET = 20

def load_image(image_path):
  return cv2.imread(image_path)

def visualize_court(dimensions, corners, players):
    image = np.zeros((dimensions[1], dimensions[0], 3))

    for corner in corners:
        cv2.circle(image, corner, radius=5, color=(0, 255, 0), thickness=2)

    for player in players:
        cv2.circle(image, player, radius=5, color=(255, 0, 0), thickness=2)

    cv2.imshow('court', image)
    cv2.waitKey()

if __name__ == "__main__":
    image = load_image(IMAGE_PATH)
    camera_corners = detect_corners(image)
    warped_court_corners = get_warped_court_corners(WARPED_COURT_DIM, WARPED_COURT_DIM_OFFSET)
    warped_y_middle = get_middle_of_warped_court(warped_court_corners)

    transformation_matrix = get_transformation_matrix(camera_corners, warped_court_corners)

    transformed_players = []
    for player in PLAYERS:
        transformed_player = warp_point(player, transformation_matrix)
        player_type = get_player_type(transformed_player, warped_court_corners, warped_y_middle)
        if player_type != 2:
            transformed_players.append(transformed_player)

    visualize_court(
            (WARPED_COURT_DIM[0] + (2 * WARPED_COURT_DIM_OFFSET), WARPED_COURT_DIM[1] + (2 * WARPED_COURT_DIM_OFFSET)), 
            warped_court_corners, 
            transformed_players
            )

