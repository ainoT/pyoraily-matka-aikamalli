# -*- coding: cp1252 -*-
# GPS-pisteiden rajaaminen tutkimusalueelle

import arcpy
import os
from arcpy import env
arcpy.env.overwriteOutput = True

input_fp = r"[dir_fp]"

# listaa trackit
def filepaths(inFolder):
    fullPaths = []
    for root, dirs, files in os.walk(inFolder):
        for filename in files:
            if filename.endswith(".shp"):
                fullpath = os.path.join(root, filename)
                fullPaths.append(fullpath) # adds filepaths to the list
    return fullPaths 

files = filepaths(input_fp)
pk_bufferi = r"[fp]"
verkosto = r"[fp]"
spatial_ref = arcpy.Describe(verkosto).spatialReference # tallennetaan verkoston koordinaatisto spatial_ref-muuttujaan

# Polku output geodatabaseen
out_fp = r"[gdb_fp]"

# luodaan gdb projisoiduille GPS-pisteille
if not arcpy.Exists(out_fp): # jos ei ole jo olemassa
    arcpy.CreateFileGDB_management(r"[dir_fp]","GPS.gdb")


# Projisoidaan gps-pisteet verkston koordinaatistoon (KKJ2, EPSG 2392)
for shape in files:
    filename = os.path.basename(shape)
    newname = "C" + filename.replace(".shp","") # nimi ei voi alkaa numerolla, siksi C alkuun
    kkj_file = os.path.join(kkj_fp,newname)
    arcpy.Project_management(shape, kkj_file, spatial_ref, "KKJ_To_WGS_1984_2_JHS153")

    
# Määritetään workspace
workspace = r"[fp]GPS.gdb"
arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True # Sallitaan ylikirjoitus
    
kkj_List = arcpy.ListFeatureClasses()

pk_bufferi = r"[fp]"

for x in kkj_List:
    lyrname = x + "_lyr" 
    # GPS shapefileista layerit jotta voi tehdä select by locationin
    lyr = arcpy.MakeFeatureLayer_management(x, lyrname)
    # Rajataan pisteet tutkimusalueelle pk-seudun kuntien 5 km bufferilla
    arcpy.SelectLayerByLocation_management(lyr, "INTERSECT","","","NEW_SELECTION","INVERT") # käännetään valinta invertilla
    # Jos alueen ulkopuolisia pisteitä on valittuna, ne poistetaan
    if int(arcpy.GetCount_management(lyr).getOutput(0)) > 0:
        arcpy.DeleteFeatures_management(lyr)
        print(lyr) # tulostetaan poistetun nimi







