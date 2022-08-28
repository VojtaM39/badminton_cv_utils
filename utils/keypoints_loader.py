import cv2
import json

def get_person_boundaries(keypoints):
  max_x = -1
  max_y = -1
  min_x = 9999
  min_y = 9999
  
  for point in keypoints:
    if point[0] > max_x:
      max_x = point[0]
    
    if point[0] < min_x and point[0] != 0:
      min_x = point[0]
      
    if point[1] > max_y:
      max_y = point[1]
    
    if point[1] < min_y and point[1] != 0:
      min_y = point[1]
    
  height = max_y - min_y
  max_y = int(max_y + (height * 0.1))
  min_y = int(min_y - (height * 0.125))

  x_len = max_x - min_x
  y_len = max_y - min_y

  if x_len > y_len:
    diff = x_len - y_len
    min_y = min_y - (diff // 2)
    max_y = max_y + (diff // 2)
  else:
    diff = y_len - x_len
    min_x = min_x - (diff // 2)
    max_x = max_x + (diff // 2)
  
  return int(max_x), int(min_x), int(max_y), int(min_y)
  
def visualize_person(image, keypoints):
  def get_int_point(float_point):
    return (int(float_point[0]), int(float_point[1]))
  
  max_x, min_x, max_y, min_y = get_person_boundaries(keypoints)
  
  cv2.line(image, (min_x, min_y), (max_x, min_y), (255, 0, 0), 2)
  cv2.line(image, (min_x, min_y), (min_x, max_y), (255, 0, 0), 2)
  cv2.line(image, (max_x, min_y), (max_x, max_y), (255, 0, 0), 2)
  cv2.line(image, (min_x, max_y), (max_x, max_y), (255, 0, 0), 2)

def visualize_frame(video_path, frame_num, people = None):
  vidcap = cv2.VideoCapture(video_path)
  vidcap.set(1, frame_num)
  _, frame = vidcap.read()

  if people is not None:
    for person in people:
      if person is not None:
        visualize_person(frame, person)
  
  return frame
    
def parse_keypoints(keypoints, keypoints_count):
  # Create tuples for each keypoint
  result = []
  for idx in range(keypoints_count):
    result.append((keypoints[idx * 3], keypoints[idx * 3 + 1]))
  return result
  
def get_bottom_person(people, center_borders):
  # Get person with point 1 closest to the bottom
  left_border, right_border = center_borders
  
  current_max = -1;
  current_max_index = None
  for idx, person in enumerate(people):
    x = person[8][0]
    y = person[8][1]
      
    
    if y > current_max and x > left_border and x < right_border:
      current_max = y
      current_max_index = idx
  
  if current_max_index != None:
    return people[current_max_index]
    
  return None

def get_top_person(people, bottom, center_borders):
  if bottom is None:
    return None

  bottom_y = bottom[8][1]
  # Get second most bottom person within borders
  left_border, right_border = center_borders
  
  current_max = -1;
  current_max_index = None
  for idx, person in enumerate(people):
    x = person[8][0]
    y = person[8][1]
    
    if y > current_max and y != bottom_y and x > left_border and x < right_border:
      current_max = y
      current_max_index = idx
  
  if current_max_index != None:
    return people[current_max_index]
    
  return None
  
  
def get_center_borders(video_path, bottom = False):
  vidcap = cv2.VideoCapture(video_path)
  vidcap.set(1, 1)
  _, frame = vidcap.read()

  _, width, _ = frame.shape

  if bottom:
    center_ratio = 0.1
  else:
    center_ratio = 0.25
    
  return (int(width * center_ratio), int(width * (1 - center_ratio)))

MAX_ATTEMPTS = 10
  
def get_keypoints(openpose_keypoints_path, frame_num):
  number_with_zeros = str(frame_num).rjust(12, '0')
  file_path = openpose_keypoints_path.format(number_with_zeros)
  
  for idx in range(10):
    try:
      with open(file_path, 'r') as file:
        data = file.read()
        parsed = json.loads(data)
      
        people_keypoints = []
        for person in parsed['people']:
          parsed_person_keypoints = parse_keypoints(person['pose_keypoints_2d'])
          people_keypoints.append(parsed_person_keypoints)
          
        return people_keypoints
        
    except Exception as e:
      print(e)
      idx += 1
      print('Attempt {} to load {} failed'.format(idx, file_path))
  return None
