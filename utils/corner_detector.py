import cv2
import numpy as np
import math

def mask_image(image):
  LOWER_THRESHOLD = 220
  UPPER_THRESHOLD = 255
  lower = np.uint8([LOWER_THRESHOLD, LOWER_THRESHOLD, LOWER_THRESHOLD])
  upper = np.uint8([UPPER_THRESHOLD, UPPER_THRESHOLD, UPPER_THRESHOLD])
  return cv2.inRange(image, lower, upper)

def get_lines(image):
  rho = 1  # distance resolution in pixels of the Hough grid
  theta = np.pi / 180  # angular resolution in radians of the Hough grid
  threshold = 13  # minimum number of votes (intersections in Hough grid cell)
  min_line_length = 20  # minimum number of pixels making up a line
  max_line_gap = 10  # maximum gap in pixels between connectable line segments
  
  return cv2.HoughLinesP(image, rho, theta, threshold, np.array([]),
                      min_line_length, max_line_gap)

def get_blurred_image(image):
  return cv2.GaussianBlur(image, (13, 13), 0)

def get_distance(line):
    x1,y1,x2,y2 = line[0]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def is_vertical(line):
    x1,y1,x2,y2 = line[0]
    return abs(y1 - y2) > abs(x1 - x2)
  
def get_max_distance(lines, vertical = None):
  curr_max = -1
  for line in lines:
    if (vertical is not None):
      if vertical != is_vertical(line):
        continue
        
    curr_max = max(curr_max, get_distance(line))
  return curr_max

def filter_lines(lines, threshold):
  filtered_lines = []
  for line in lines:
    size = get_distance(line)
    if (size > threshold):
      filtered_lines.append(line)
  return filtered_lines

def get_vertical_outer_lines(lines, max_size):
  # ((top), (bot))
  max = ((-1, None), (-1, None))
  min = ((float('inf'), None), (float('inf'), None))
  for line in lines:
    if not is_vertical(line):
      continue
    
    if get_distance(line) < 0.4 * max_size:
      continue

    x1, y1, x2, y2 = line[0]
    if y1 > y2:
      curr = ((x1, y1), (x2, y2))
    else:
      curr = ((x2, y2), (x1, y1))

    if curr[0][0] > max[0][0] and curr[1][0] > max[1][0]:
      max = curr
    elif curr[0][0] < min[0][0] and curr[1][0] < min[1][0]:
      min = curr
    
  return [min, max]

def get_vertical_lines(lines):
  result = []
  for line in lines:
    if is_vertical(line):
      result.append(line)
  return result

def is_actual_court(height, width, left_bot, left_top, right_bot, right_top):
  MIN_RATIO_TOP = 0.2
  MIN_RATIO_BOTTOM = 0.4
  MIN_RATIO_VERTICAL = 0.3
  
  top_width = abs(right_top[0] - left_top[0])
  bottom_width = abs(right_bot[0] - left_bot[0])
  left_height = abs(left_bot[1] - left_top[1])
  right_height = abs(right_bot[1] - right_top[1])
  
  if top_width < width * MIN_RATIO_TOP:
    return False
    
  if bottom_width < width * MIN_RATIO_BOTTOM:
    return False
    
  min_height = height * MIN_RATIO_VERTICAL
  
  if left_height < min_height:
    return False
    
  if right_height < min_height:
    return False

  return True

def create_line_image(image, lines):
  height, width, _ = image.shape
  canvas = np.zeros((height, width, 3), dtype=np.uint8)
  for line_wrapper in lines:
    line = line_wrapper[0]
    cv2.line(canvas, (line[0], line[1]), (line[2], line[3]), (255, 255, 255), 2)
  return canvas


def detect_corners(image):
    """
    Returns:
        points(tuple): corner points of court (bottom_left, bottom_right, top_left, top_right)
    """
    try:
        height, width, _ = image.shape
        
        masked_image = mask_image(image)
        lines = get_lines(masked_image)
        filtered_lines = filter_lines(lines, 0.1 * get_max_distance(lines))
        vertical_lines = get_vertical_lines(filtered_lines)
        
        line_image = create_line_image(image, vertical_lines)
        masked_image = mask_image(line_image)
        blured_image = get_blurred_image(masked_image)
        lines = get_lines(blured_image)
        
        max_distance_vertical = get_max_distance(lines, True)
        outer_lines = get_vertical_outer_lines(lines, max_distance_vertical)

        left_bot = outer_lines[0][0]
        left_top = outer_lines[0][1]
        right_bot = outer_lines[1][0]
        right_top = outer_lines[1][1]

        is_court = is_actual_court(height, width, left_bot, left_top, right_bot, right_top)

        if not is_court:
            return None

        return (left_top, right_top, left_bot, right_bot)
    except Exception as e:
        print('detect_corners failed on:')
        print(e)
        return None

