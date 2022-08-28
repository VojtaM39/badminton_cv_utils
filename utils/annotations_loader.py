import xml.etree.ElementTree as ET

def get_frame_from_milliseconds(milliseconds):
  return int(milliseconds / 1000 * FRAME_RATE

def load_annotations(annotation_file):
  tree = ET.parse(annotation_file)
  root = tree.getroot()

  # Parse time slots
  time_orders = dict()
  for child in root:
    if child.tag == 'TIME_ORDER':
      for time_element in child:
        time_orders[time_element.attrib['TIME_SLOT_ID']] = get_frame_from_milliseconds(int(time_element.attrib['TIME_VALUE']))
  
  annotations = []
  for child in root:
    if child.tag == 'TIER' and child.attrib['TIER_ID'] in ['fineanno', 'shotanno']:
      for annotation in child:
        # Check annotation value
        annotation_val = annotation[0][0].text
        if annotation_val in ANNOTATIONS_TO_KEEP_TOP or annotation_val in ANNOTATIONS_TO_KEEP_BOTTOM:
          annotations.append(
              {
                'ref1': time_orders[annotation[0].attrib['TIME_SLOT_REF1']],
                'ref2': time_orders[annotation[0].attrib['TIME_SLOT_REF2']],
                'value': annotation_val
              }
          )


