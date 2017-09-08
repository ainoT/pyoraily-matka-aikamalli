# -*- coding: cp1252 -*-
# GPS-pisteiden aika, matka ja nopeustiedot
# Track Intervals to Features (Tracking Analyst)

import arcpy
arcpy.CheckOutExtension("tracking")
import os
from arcpy import env
arcpy.env.overwriteOutput = True

# Filepath for input features
inFolder = r"{dir_fp}"

# Iterate input filepaths and add them to a list
def filepaths(inFolder):
    fullPaths = []
    for root, dirs, files in os.walk(inFolder):
        for filename in files:
            if filename.endswith(".shp"):
                fullpath = os.path.join(root, filename)
                fullPaths.append(fullpath) # adds filepaths to the list
    return fullPaths 

# Define 'track intervals to feature' parameters
time_field = "DateTimeS"
calculation_method = "PREVIOUS_AND_CURRENT_FEATURE"
time_field_format = "YYYY-MM-DD hh:mm:ss"
distance_field_units = "METERS"
distance_field_name = "DISTANCE_m"
duration_field_units = "SECONDS"
duration_field_name = "DURATION_s"
speed_field_units = "METERS_PER_SECOND"
speed_field_name = "SPEED_mps"
course_field_units = "DEGREES"
course_field_name = "Bearing"

files = filepaths(inFolder)

# Iterate input files
for track in files:
    filename = os.path.basename(track)                                            # erotetaan tiedostonimi
    newname = str(filename.replace(".shp",""))                                    # poistetaan shp-p��te ja muutetaan string-tyypiksi
    name_expression = "'" + newname + "'"                                         # lis�t��n hipsut jotta p�ivittyy oikein
    arcpy.AddField_management(track, "Trackname", "TEXT")                         # lis�t��n Trackname-kentt�
    arcpy.CalculateField_management(track, "Trackname", name_expression,"PYTHON_9.3")  # lis�t��n tiedoston nimi Trackname-kentt��n
    arcpy.AddField_management(track, "CycID", "SHORT")                            # Lis�t��n py�r�ilij�n ID-numero ominaisuustiedoksi
    namesplit = filename.split("_")                                               # erotetaan py�r�ilj�n ID-numero
    numsplit = namesplit[0].split("C")
    ID_expression = numsplit[1]
    arcpy.CalculateField_management(track, "CycID", int(ID_expression))           # lis�t��n CycID-numero integerina
    arcpy.CalculateField_management (track, "Id", expression="[FID] + 1")         # lasketaan viel� jokaiselle pisteelle oma Id-numero
    # Track intervals to feature
    arcpy.TrackIntervalsToFeature_ta(track, time_field, "", calculation_method, time_field_format, "", "", "", distance_field_units, distance_field_name, duration_field_units, duration_field_name, speed_field_units, speed_field_name, course_field_units, course_field_name)


