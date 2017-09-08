# -*- coding: cp1252 -*-
# Reittipisteiden poistaminen 200 m matkalta reitin alusta ja lopusta

import arcpy

workspace = r"[filepath]"
arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True # Sallitaan ylikirjoitus

# Listataan workspacessa olevat feature classit
fcList = arcpy.ListFeatureClasses()

for track in fcList:
    # List all of the row values as a list
    rows = [row[0] for row in arcpy.da.SearchCursor(track, "from_start")]
    # haetaan viimeinen arvo listasta ja muutetaan float-tyypiksi
    last_row = float(rows[-1]) 
    # Tehdään UpdateCursor rivien poistamiseksi
    with arcpy.da.UpdateCursor(track,["from_start"]) as cursor:
            for row in cursor:
                if row[0]<=200:             # jos arvo <= 200m, poistetaan
                    cursor.deleteRow()
                if row[0]>=(last_row-200):  # jos arvo < 200 m lopusta, poistetaan
                    cursor.deleteRow()



