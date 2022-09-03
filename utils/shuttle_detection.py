import numpy as np

def get_court_rectangle(frame, corners, top_offset, bottom_offset, horizontal_offset):
  """
  Returns croped court from frame
  """
  # Get max and min for X and Y
  max_x, max_y = float('-inf'), float('-inf')
  min_x, min_y = float('inf'), float('inf')

  for corner in corners:
    x, y = corner

    if x is None or y is None:
      return None
    
    if x > max_x:
      max_x = x
      
    if y > max_y:
      max_y = y
      
    if y < min_x:
      min_x = x
      
    if y < min_y:
      min_y = y
  
  max_x += horizontal_offset
  max_y += bottom_offset
  min_x -= horizontal_offset
  min_y -= top_offset

  return np.array(frame[min_y:max_y,min_x:max_x,:]), (min_x, max_x, min_y, max_y)
