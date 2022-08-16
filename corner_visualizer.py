from utils.corner_detector import detect_corners
import cv2
import numpy as np

IMAGE_PATH="./tmp/image1.png"

def load_image(image_path):
  return cv2.imread(image_path)

def get_overlay(image, corners):
    for corner in corners:
        cv2.circle(image, corner, radius=5, color=(0, 255, 0), thickness=2)

def visualize_corners(image_path):
    image = load_image(IMAGE_PATH)
    cv2.imshow('Pre-detection', image)
    cv2.waitKey()

    corners = detect_corners(image)
    get_overlay(image, corners)

    cv2.imshow('Post-detection', image)
    cv2.waitKey()

if __name__ == "__main__":
    visualize_corners(IMAGE_PATH)
