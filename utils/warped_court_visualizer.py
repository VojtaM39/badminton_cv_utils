import cv2
import numpy as np

def visualize_court(dimensions, corners, players):
    image = np.zeros((dimensions[1], dimensions[0], 3))

    for corner in corners:
        cv2.circle(image, corner, radius=5, color=(0, 255, 0), thickness=2)

    for player in players:
        cv2.circle(image, player, radius=5, color=(255, 0, 0), thickness=2)

    return image
