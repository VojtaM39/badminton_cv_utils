import cv2
import numpy as np

TYPE_PLAYER_BOTTOM = 0
TYPE_PLAYER_TOP = 1
TYPE_NOT_PLAYER = 2

def get_warped_court_corners(warped_court_dim, warped_court_offset):
    corners = []
    for height_offset in [0, 1]:
        for width_offset in [0, 1]:
            corners.append((
              warped_court_dim[0] * width_offset + warped_court_offset,
              warped_court_dim[1] * height_offset + warped_court_offset,
            ))
    return corners

def warp_point(point, M):
    x, y = point
    d = M[2, 0] * x + M[2, 1] * y + M[2, 2]

    return (
        int((M[0, 0] * x + M[0, 1] * y + M[0, 2]) / d), # x
        int((M[1, 0] * x + M[1, 1] * y + M[1, 2]) / d), # y
    )

def get_transformation_matrix(camera_corners, warped_court_corners):
    return cv2.getPerspectiveTransform(np.float32(camera_corners), np.float32(warped_court_corners))

def get_middle_of_warped_court(corners):
    return (corners[2][1] - corners[0][1]) // 2 + corners[0][1]

def get_player_type(player, corners, y_middle):

    # Check for x overflow
    if player[0] < corners[0][0] or player[0] > corners[1][0]:
        return TYPE_NOT_PLAYER

    # Check for y overflow
    if player[1] < corners[0][1] or player[1] > corners[2][1]:
        return TYPE_NOT_PLAYER

    if player[1] < y_middle:
        return TYPE_PLAYER_TOP

    return TYPE_PLAYER_BOTTOM

