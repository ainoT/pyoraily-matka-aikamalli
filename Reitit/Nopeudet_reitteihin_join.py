# -*- coding: cp1252 -*-
# Joinataan R:ll� aggregoidut segmenttien nopeustiedot takaisin reitteihin

import arcpy
import os
arcpy.env.overwriteOutput = True

# M��ritet��n p��hakemisto      
ws_dir = r"[dir_fp]"
# Reittihakemisto
reitti_fp = os.path.join(ws_dir,"Reitit.gdb")
# M��ritet��n workspace
arcpy.env.workspace = reitti_fp

# Listataan reittitiedostot
reittilista = arcpy.ListFeatureClasses("","","Tieverkkojoin")

# Haetaan R:ss� muokattu ja ArcMapissa tableksi muunnettu segmenttitiedosto
table = "Segmentit_nopeudet"

# M��ritet��n polku tuloksille
out_fp = os.path.join(reitti_fp,"Nopeusjoin")


# Iteroidaan reittej�
for reitti in reittilista[3:]:
    print(reitti)
    # Lis�t��n samanlainen segmentID-kentt� kuin segmenteill� taulukossa
    arcpy.AddField_management(reitti, "segID", "TEXT", "", "", 100)
    # Lasketaan kentt��n segmentID arvo
    arcpy.CalculateField_management(reitti, "segID", 'str(!CycID!) + " " + !Name! + " " + str(!TARGET_FID!)', "PYTHON_9.3")
    # Tehd��n reitist� layer
    reitti_lyr = reitti.replace("vayla","lyr")
    arcpy.MakeFeatureLayer_management(reitti,reitti_lyr)
    # Joinataan reittiin tiedot segmenttitaulukosta
    arcpy.AddJoin_management(reitti_lyr, "segID", table, "segmentID")
    # Kopioidaan tulos
    output = os.path.join(out_fp,reitti.replace("vayla","nop"))
    arcpy.CopyFeatures_management(reitti_lyr, output)
    # Poistetaan lyr
    arcpy.Delete_management(reitti_lyr)

