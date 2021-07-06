# IRM YOLOV5

This repo contains an example of how Python is used to reformat Unity's rendered training data with the eventual goal of training yolo V5 using this data set. More specifically, the goal is to produce training data in the **COCO JSON** format, before exporting this data to Roboflow.

The structure of this repo is as follows
* groceries_unity -> This folder contains three folders that are the output from Unity
* script.py -> This is the pyhton script that is doing the work
* log.json -> This log file can be used for logging errors or just general debugging

## groceries_unity
From the three folders contained here, only the "Dataset-" and "RGB-" folders are used. The first contains a set of JSON files and the latter contains all the redered images. The JSON files describe the annotations of objects displayed in the images and these annotations are linked to specific image filenames. The JSON files that are of interest are:
* metric_definitions.json
* captures_000.json and captures_001.json -> More of these files appear with increasing data set size.

The metric definitions is a list of label_id's paired with label names. And the "captures-" files contain lists of annotations that reference the metric definitions and relevant images.

## script.py
After making the neccessary imports, the structure for COCO JSON is defined with the initialization of the output dictionary named "outdata". This is followed by opening the metric definitions file and adding the list of definitions as the value to the "categories" key in the "outdata" dictionary. Next, the information contained in the "captures-" files is extracted and they are all added to the same list called "captures_batches".

Now the bulk of the work is done by looping through the above mentioned list to extract the required information. Contained in that loop, images from the "RGB-" folder are opened to find their widths, heights and creation timestamps. An "img_instance" is made for every image, containing the required information, and then appended to the "images" key of the "outdata" dictionary. Similarly, instances of the annotations data is appended in the correct structure to the "annotations" key of that dictionary.

Finally, the "outdata" dictionary is written to an output.json file in the "RGB-" folder. This is the only file in that folder that is not an image, which is the exact format that is required by Roboflow.

## log.json
This can be used in whatever way required to display debugging data and does not affect anything else.

# Things to consider when using script.py with a new data set from Unity
### Folder Names
The "Dataset-" and "RGB-" folders will have new names every time. Update the names in the script.
### Number of "captures-" files
The number of "captures-" files could be different depending on the size of the data set. Be sure to read all of them in the section labelled "FETCH THE CAPTURES FILES" in script.py.
