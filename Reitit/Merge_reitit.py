# -*- coding: cp1252 -*-
# Mergetään nopeustiedot sisältävät reitit samaan
import arcpy
import os
arcpy.env.overwriteOutput = True

# Määritetään päähakemisto      
ws_dir = r"[dir_fp]"
# GPS-pisteiden hakemisto
reitti_fp = os.path.join(ws_dir,"Reitit.gdb")
# Määritetään output-hakemisto
grid_fp = os.path.join(ws_dir,"Ruututarkastelu.gdb")

# Määritetään työtila
arcpy.env.workspace = reitti_fp
# Listataan reitit
reittiList = arcpy.ListFeatureClasses("","","Nopeusjoin")

# Määritellään output
out_fp = os.path.join(grid_fp,"Merge")
reittimerge = os.path.join(out_fp,"Reitit_merge")

# Fieldmappings
fieldmappings = arcpy.FieldMappings()

for reitti in reittiList:
    fieldmappings.addTable(reitti)

    # Add input fields into new output field
    fldMap_speed = arcpy.FieldMap()
    fldMap_speed.addInputField(reitti,"Segmentit_nopeudet_SPEED_mps_x")
    # Set name of new output field
    speedName = fldMap_speed.outputField
    speedName.name = "Mediaaninopeus"
    speedName.aliasName = "Mediaaninopeus"
    fldMap_speed.outputField = speedName
    # Set the merge rule
    fldMap_speed.mergeRule = "MEDIAN"

    # Remove all unneccessary output fields from the field mappings
    saastettavat = ["Segmentit_nopeudet_Nimi", "Segmentit_nopeudet_segmentID", "Segmentit_nopeudet_SPEED_mps_x", "Segmentit_nopeudet_Gradientti", "Segmentit_nopeudet_Reittipituus", "Segmentit_nopeudet_Rist_lv", "Segmentit_nopeudet_Rist_auto", "Segmentit_nopeudet_Rist_kevyt", "Segmentit_nopeudet_Rist_yht", "Segmentit_nopeudet_H_LEVEL", "Segmentit_nopeudet_luokka_oma", "Segmentit_nopeudet_Tieluokitus", "Segmentit_nopeudet_Pyoravayla", "Segmentit_nopeudet_Speed_md", "Segmentit_nopeudet_Speed_min", "Segmentit_nopeudet_Speed_max", "Segmentit_nopeudet_Speed_sd", "Segmentit_nopeudet_matka", "Segmentit_nopeudet_aika", "Segmentit_nopeudet_Count_gps", "Segmentit_nopeudet_SPEED_mps_y", "Segmentit_nopeudet_SPEED_mps", "Segmentit_nopeudet_Nop_ka_ero", "Segmentit_nopeudet_Nop_md_ero", "Mediaaninopeus"]
    for field in fieldmappings.fields:
        if field.name not in saastettavat:
            fieldmappings.removeFieldMap(fieldmappings.findFieldMapIndex(field.name))

# Add output field to field mappings object
fieldmappings.addFieldMap(fldMap_speed)


# Mergetään kaikki reitit yhdeksi
arcpy.Merge_management(reittiList, reittimerge, fieldmappings)


