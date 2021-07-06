import json
import os
import time
from PIL import Image
from datetime import date


#########################################################################
#################### DEFINE COCO JSON STRUCTURE #########################
#########################################################################


outdata = {
    "info": {
        "year": "2021",
        "version": 1,
        "description": "Converted in Py from Unity",
        "contributor": "Daniel Moller",
        "url": "",
        "date_created": str(date.today())
    },
    "licenses": [
        {
            "id": 1,
            "url": "",
            "name": "Unknown"
        }
    ],
    "images": [],
    "annotations": [],
    "categories": [
        {
            "id": 0,
            "name": "groceries",
            "supercategory": "none"
        }
    ]
}


#########################################################################
################## FETCH THE METRIC DEFINITIONS FILE ####################
#########################################################################


with open('groceries_unity/Dataset731f0111-624c-429a-ac6a-d5b5bb43f3ed/metric_definitions.json') as categories_json_file:
    categories_data = json.load(categories_json_file)
    for x in categories_data['metric_definitions']:
        if x['name'] == 'object count':
            categories = x['spec']
            for cat in categories:
                category_instance = {
                    "id": cat['label_id'],
                    "name": cat['label_name'],
                    "supercategory": "groceries"
                }
                outdata['categories'].append(category_instance)


#########################################################################
#################### FETCH THE CAPTURES FILES ###########################
#########################################################################

# Add a "with open" block for every "captures-" file and add to "captures_batches"

captures_batches = []

# fetch first captures file
with open('groceries_unity/Dataset731f0111-624c-429a-ac6a-d5b5bb43f3ed/captures_000.json') as json_file:
    data = json.load(json_file)
    captures_instance = data['captures']
    captures_batches.append(captures_instance)

# fetch second captures file
with open('groceries_unity/Dataset731f0111-624c-429a-ac6a-d5b5bb43f3ed/captures_001.json') as json_file:
    data = json.load(json_file)
    captures_instance = data['captures']
    captures_batches.append(captures_instance)


#########################################################################
#################### EXTRACT RELEVANT INFORMATION #######################
#########################################################################


# Initialize logging variables
log = {}
num_files_with_annotations = 0

for captures in captures_batches:

    for capture in captures:
        
        try:
            capture_id = capture['id']
            filename = capture['filename']
            values = capture['annotations'][0]['values']
            print('')
            print("FILE NAME: " + filename)
        except KeyError as err:
            print('Dictionary key not found! ---> ' + err)
            log['dictionary_not_found'] = []
            log['dictionary_not_found'].append(filename)
            continue

        # get image size and date created
        image = Image.open("groceries_unity/" + filename)
        img_width, img_height = image.size
        ti_c = os.path.getctime("groceries_unity/" + filename)
        c_ti = time.ctime(ti_c)

        # Add image data to output
        img_instance = {
            "id": capture_id,
            "license": 1,
            "width": img_width,
            "height": img_height,
            "file_name": filename,
            "date_captured": c_ti
        }
        outdata['images'].append(img_instance)

        if len(values) > 0:

            num_files_with_annotations += 1

            for box in values:
                # print(box['label_name'])

                # add annotation data to output
                annotation_instance = {
                    "id": box['instance_id'],
                    "category_id": box['label_id'],
                    "iscrowd": 0,
                    "segmentation": [],
                    "image_id": capture_id,
                    "area": box['width'] * box['height'],
                    "bbox": [box['x'], box['y'], box['width'], box['height']]
                }
                outdata['annotations'].append(annotation_instance)
        
        else:
            log['no_annotations'] = []
            log['no_annotations'].append(filename)
            

log['files_with_annotations'] = []
log['files_with_annotations'].append(num_files_with_annotations)


#########################################################################
################### WRITE THE NECCESSARY OUTPUT #########################
#########################################################################


with open('groceries_unity/RGB80994f29-b2a1-4884-9bbe-c563698a76d3/output.json', 'w') as outfile:
    json.dump(outdata, outfile)

# Used for debugging
with open('log.json', 'w') as logfile:
    json.dump(log, logfile)

        



    