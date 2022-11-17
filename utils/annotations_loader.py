import xml.etree.ElementTree as ET
import csv
import json

def get_frame_from_milliseconds(milliseconds, frame_rate):
  return int(milliseconds / 1000 * frame_rate)

def load_annotations(annotation_file, frame_rate):
  tree = ET.parse(annotation_file)
  root = tree.getroot()

  # Parse time slots
  time_orders = dict()
  for child in root:
    if child.tag == 'TIME_ORDER':
      for time_element in child:
        time_orders[time_element.attrib['TIME_SLOT_ID']] = get_frame_from_milliseconds(int(time_element.attrib['TIME_VALUE']), frame_rate)
  
  annotations = []
  for child in root:
    if child.tag == 'TIER' and child.attrib['TIER_ID'] in ['fineanno', 'shotanno']:
      for annotation in child:
        # Check annotation value
        annotation_val = annotation[0][0].text
        annotations.append(
          {
            'ref1': time_orders[annotation[0].attrib['TIME_SLOT_REF1']],
            'ref2': time_orders[annotation[0].attrib['TIME_SLOT_REF2']],
            'value': annotation_val
          }
        )

  return annotations

def load_via_annotations(annotation_file, frame_rate):
    annotations = []
    with open(annotation_file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                ref1 = int(float(row['temporal_segment_start']) * frame_rate)
                ref2 = int(float(row['temporal_segment_end']) * frame_rate)

                metadata = json.loads(row['metadata'])
                value = metadata['TEMPORAL-SEGMENTS']
            except:
                continue

            if value == 'default':
                continue

            annotations.append({
                'ref1': ref1,
                'ref2': ref2,
                'value': value,
            })
    return annotations
