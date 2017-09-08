# -*- coding: cp1252 -*-
# Lasketaan tiesegmenttien ajoajat eri pyöräilijätyypeille ja hidastetuille osuuksille

import arcpy
import os
import shutil
from arcpy import env

env.overwriteOutput = True

# Haetaan pyöräverkoston tiedostopolku
fp_reititys = "[filepath]"
env.workspace = fp_reititys
tieverkko = os.path.join(fp_reititys,"Pyoraily_E","pyorailyverkko_E_tm35fin")

# Lisätään kentät eri pyöräilijätyyppien vakionopeuksille
arcpy.AddField_management(tieverkko, "Nop3", "SHORT") # "peruspyöräilijä", aktiivisuus 3, nopeus 18 km/h
arcpy.AddField_management(tieverkko, "Nop4", "SHORT") # "rivakka arkipyöräilijä", aktiivisuus 4, nopeus 22 km/h
arcpy.AddField_management(tieverkko, "Nop5", "SHORT") # "aktiivipyöräiljä", aktiivisuus 5, nopeus 24 km/h

# Lisätään kentät keskustan hidastettaville nopeuksille
arcpy.AddField_management(tieverkko, "Nop3hidaste", "DOUBLE") # "peruspyöräilijä", aktiivisuus 3, nopeus hidastettavissa ruuiduissa 0,8*18 km/h
arcpy.AddField_management(tieverkko, "Nop4hidaste", "DOUBLE") # "rivakka arkipyöräilijä", aktiivisuus 4, nopeus hidastettavissa ruuiduissa 0,8*22 km/h
arcpy.AddField_management(tieverkko, "Nop5hidaste", "DOUBLE") # "aktiivipyöräiljä", aktiivisuus 5, nopeus hidastettavissa ruuiduissa 0,8*24 km/h

# Lasketaan nopeudet
arcpy.CalculateField_management(tieverkko, "Nop3", 18, "PYTHON") 
arcpy.CalculateField_management(tieverkko, "Nop4", 22, "PYTHON")
arcpy.CalculateField_management(tieverkko, "Nop5", 24, "PYTHON")

## Valitaan ne segmentit joihin hidaste lisätään
keskustaruudut = "[fp]"
# Tehdään feature layer
keskusta_lyr = "Keskusta_lyr"
arcpy.MakeFeatureLayer_management(keskustaruudut, keskusta_lyr)
# Valitaan ruuduista ne, joiden nopeus on keskinopeutta 6.3 m/s hitaampi
arcpy.SelectLayerByAttribute_management(keskusta_lyr, "NEW_SELECTION", 'Keskinopeus < 6.3')
# Valitaan tiesegmenteistä ne jotka ovat kyseisten ruutujen sisällä
tieverkko_lyr = "Tieverkko_lyr"
arcpy.MakeFeatureLayer_management(tieverkko, tieverkko_lyr)
arcpy.SelectLayerByLocation_management(tieverkko_lyr, "HAVE_THEIR_CENTER_IN", keskusta_lyr)
# Lasketaan nopeudet valituille segmenteille
arcpy.CalculateField_management(tieverkko_lyr, "Nop3hidaste", '0.8*18', "PYTHON")
arcpy.CalculateField_management(tieverkko_lyr, "Nop4hidaste", '0.8*22', "PYTHON")
arcpy.CalculateField_management(tieverkko_lyr, "Nop5hidaste", '0.8*24', "PYTHON")
# Käännetään valinta
arcpy.SelectLayerByLocation_management(tieverkko_lyr, "WITHIN", keskusta_lyr, "", "SWITCH_SELECTION")
# Lasketaan nopeus "normaaleille" segmenteille
arcpy.CalculateField_management(tieverkko_lyr, "Nop3hidaste", 18, "PYTHON")
arcpy.CalculateField_management(tieverkko_lyr, "Nop4hidaste", 22, "PYTHON")
arcpy.CalculateField_management(tieverkko_lyr, "Nop5hidaste", 24, "PYTHON")
# Poistetaan valinnat
arcpy.SelectLayerByAttribute_management(tieverkko_lyr, "CLEAR_SELECTION")

# Lisätään kentät ajoajoille
arcpy.AddField_management(tieverkko, "Aika3", "DOUBLE") 
arcpy.AddField_management(tieverkko, "Aika4", "DOUBLE") 
arcpy.AddField_management(tieverkko, "Aika5", "DOUBLE")
arcpy.AddField_management(tieverkko, "Aika3hidaste", "DOUBLE")
arcpy.AddField_management(tieverkko, "Aika4hidaste", "DOUBLE")
arcpy.AddField_management(tieverkko, "Aika5hidaste", "DOUBLE")

# Lasketaan matka-aika minuutteina
arcpy.CalculateField_management(tieverkko, "Aika3", "(!Shape_Length! / (!Nop3! / 3.6)) / 60", "PYTHON") 
arcpy.CalculateField_management(tieverkko, "Aika4", "(!Shape_Length! / (!Nop4! / 3.6)) / 60", "PYTHON")
arcpy.CalculateField_management(tieverkko, "Aika5", "(!Shape_Length! / (!Nop5! / 3.6)) / 60", "PYTHON")
arcpy.CalculateField_management(tieverkko, "Aika3hidaste", "(!Shape_Length! / (!Nop3hidaste! / 3.6)) / 60", "PYTHON")
arcpy.CalculateField_management(tieverkko, "Aika4hidaste", "(!Shape_Length! / (!Nop4hidaste! / 3.6)) / 60", "PYTHON")
arcpy.CalculateField_management(tieverkko, "Aika5hidaste", "(!Shape_Length! / (!Nop5hidaste! / 3.6)) / 60", "PYTHON")

#Check out the Network Analyst extension license
arcpy.CheckOutExtension("Network")

network = os.path.join(fp_reititys,"Pyoraily_E","Pyoraily_E_ND")

#Build the network dataset
arcpy.na.BuildNetwork(network)

#Build errors
temp_dir = os.environ.get("TEMP")
if temp_dir:
    shutil.copy2(os.path.join(temp_dir, "BuildErrors.txt"), sys.path[0])
