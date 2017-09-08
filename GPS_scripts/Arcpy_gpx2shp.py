import arcpy
import os
from arcpy import env
arcpy.env.overwriteOutput = True


gpxFolder = "[filepath]"
outputFolder = "[filepath]"


# Iterate input filepaths and add them to a list
def filepaths(gpxFolder):
    fullPaths = []
    for root, dirs, files in os.walk(gpxFolder):
        for filename in files:
            if filename.endswith(".gpx"):
                fullpath = os.path.join(root, filename)
                fullPaths.append(fullpath) # adds filepaths to the list
    return fullPaths 

files = filepaths(gpxFolder)

# Iterate input files
for track in files:
    filename = os.path.basename(track)
##    split = filename.split("_file_")
##    name = "%s" % split[1]
##    newName = name.replace(".gpx",".shp")
    newName = filename.replace(".gpx",".shp")
    # Define output path
    out_fp = os.path.join(outputFolder, newName)
    # gpx to shp conversion
    arcpy.GPXtoFeatures_conversion(track, out_fp)
        
