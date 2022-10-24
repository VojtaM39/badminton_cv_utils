from math import cos, sin, radians
import random
import cv2
import numpy as np

def get_max_edge(extremes):
  max_x, min_x, max_y, min_y = extremes
  x_dist = max_x - min_x
  y_dist = max_y - min_y
  return max(x_dist, y_dist)
  
def get_extremes(pose):
  max_x, max_y = -1, -1
  min_x, min_y = 9999, 9999

  for point in pose:
    if point == (0, 0):
      continue
    
    if point[0] > max_x:
      max_x = point[0]
      
    if point[1] > max_y: 
      max_y = point[1] 
      
    if point[0] < min_x:
      min_x = point[0]
      
    if point[1] < min_y:
      min_y = point[1]

  if max_x == -1 or max_y == -1:
    return None
    
  if min_x == 9999 or min_y == 9999:
    return None
  
  return max_x, min_x, max_y, min_y

def crop_and_center_pose(pose):
  extremes = get_extremes(pose)
  max_edge = get_max_edge(extremes)
  
  max_x, min_x, max_y, min_y = extremes

  x_offset = (max_edge - (max_x - min_x)) / max_edge
  y_offset = (max_edge - (max_y - min_y)) / max_edge
  
  relative_pose = []
  for point in pose:
    if point == (0, 0):
      relative_pose.append((0, 0))
    else:
      x = -1 + ((point[0] - min_x) / max_edge * 2) + x_offset
      y = -1 + ((point[1] - min_y) / max_edge * 2) + y_offset
      relative_pose.append((x, y))
      
  return np.array(relative_pose)
  
def get_normalized_pose(pose):
  def get_filtered_pose(pose):
    points_to_keep = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    filtered_pose = []
    for point_idx in points_to_keep:
      filtered_pose.append(pose[point_idx])
    return filtered_pose
    
  filtered_pose = get_filtered_pose(pose)
  return crop_and_center_pose(filtered_pose)

def transform_pose(pose, M):
  def warp_point(point, M):
    x, y = point
    d = M[2, 0] * x + M[2, 1] * y + M[2, 2]

    return (
        ((M[0, 0] * x + M[0, 1] * y + M[0, 2]) / d),
        ((M[1, 0] * x + M[1, 1] * y + M[1, 2]) / d)
    )

  transformed = []
  for point in pose:
    transformed.append(warp_point(point, M))
  return transformed

def trig(angle):
  r = radians(angle)
  return cos(r), sin(r)

def get_rotation_matrix(rotation):
  xC, xS = trig(rotation[0])
  yC, yS = trig(rotation[1])
  zC, zS = trig(rotation[2])
  rotate_X_matrix = np.array([[1, 0, 0],
                              [0, xC, -xS],
                              [0, xS, xC]])
  rotate_Y_matrix = np.array([[yC, 0, yS],
                              [0, 1, 0],
                              [-yS, 0, yC]])
  rotate_Z_matrix = np.array([[zC, -zS, 0],
                              [zS, zC, 0],
                              [0, 0, 1]])
  return np.dot(rotate_Z_matrix, np.dot(rotate_Y_matrix, rotate_X_matrix))

def get_scale_matrix(scale):
  return np.array([[scale[0], 0, 0],
                   [0, scale[1], 0],
                   [0, 0, 1]])

def get_random_transformation(seed, max_rotation = 0.15, max_scale=0.3):
  random.seed(seed)

  x_rotation = random.uniform(-max_rotation, max_rotation)
  y_rotation = random.uniform(-max_rotation, max_rotation)
  z_rotation = random.uniform(-max_rotation, max_rotation)

  # the pose is then normalized to -1 and 1, so we do not have to scale both axis
  scale = random.uniform(1 - max_scale, 1 + max_scale)

  rotation_matrix = get_rotation_matrix([x_rotation, y_rotation, z_rotation])
  scale_matrix = get_scale_matrix([scale, 1])

  return np.dot(rotation_matrix, scale_matrix)

