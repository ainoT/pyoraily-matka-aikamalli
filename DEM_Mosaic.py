# Korkeusmallien mosaikointi
# ArcGIS Help: Mosaic (Data Management) 


import arcpy
from arcpy import env
env.workspace = r"[fp]"



# Mosaic to new raster
input_list = "L4133A.tif;L4133B.tif;L4133C.tif;L4133D.tif;L4133F.tif;L4134C.tif;L4134E.tif;L4134D.tif;L4134F.tif;L4133E.tif;L4133H.tif;L4134G.tif;L4134A.tif;L4134B.tif;L4143A.tif;L4143C.tif;L4143E.tif;L4134H.tif;L4131G.tif;L4131E.tif;L4131F.tif;L4131H.tif;L4132G.tif;L4132H.tif;L4141G.tif;L4141E.tif;L4132F.tif;L4132D.tif;L4132E.tif;L4132C.tif;L4131D.tif;L4143B.tif;L4131C.tif"
output_fp = r"[fp]"
new_raster = "L413Mos3.tif"
# GCS_EUREF_FIN wkid 104129, TM35FIN 3067

arcpy.MosaicToNewRaster_management (input_list, output_fp, new_raster, "", "32_BIT_FLOAT", 2, 1)


