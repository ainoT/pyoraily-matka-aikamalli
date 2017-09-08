# -*- coding: cp1252 -*-

## Teiden luokittelu risteysluokitusta varten ##

import arcpy
import os
from arcpy import env
arcpy.env.overwriteOutput = True

# Määritetään workspace
env.workspace = r"[gdb_fp]"

verkosto = "pyorailyverkko_clip"
luokitus = "luokka" # uuden luokituskentän nimi

# Lisätään kenttä tieluokitukselle
arcpy.AddField_management(verkosto, luokitus, "SHORT")

## Luokitellaan tiesegmentit alkuperäisaineistojen ominaisuustietojen ja omien täydennysten perusteella

# Tehdään verkostosta feature layer
verkosto_lyr = "verkosto_lyr"
arcpy.MakeFeatureLayer_management(verkosto, verkosto_lyr)
# ehtolause auto-tyypin teiden valintaan
expression_auto = "(VAYLATYYPP>0 AND VAYLATYYPP<=3) OR (TOIMINNALL>0 AND TOIMINNALL<=6) OR (TYYPPI>0 AND TYYPPI<=4) OR rpastpartc=1 OR rpastpartc=2 OR rpastpartc=7 OR rpastpartc=10 OR V_LEVEL=2 OR V_LEVEL=1 OR H_LEVEL=3 OR H_LEVEL=4 OR H_LEVEL=30 OR luok_oma=1"
# ehtolause kevyen liikenteen tyypin teiden valintaan (POISLUKIEN PORTAAT YM. KIELLETYT)
expression_kl = "VAYLATYYPP=4 OR TOIMINNALL=10 OR TYYPPI=13 OR TYYPPI=12 OR rpastpartc=0 OR rpastpartc=4 OR rpastpartc=5 OR rpastpartc=8 OR rpastpartc>=12 OR (V_LEVEL>=4 AND V_LEVEL<=6) OR V_LEVEL>=9 OR H_LEVEL<=2 OR H_LEVEL=8 OR H_LEVEL=18 OR H_LEVEL>=62 OR luok_oma=2 OR (RPAPKPARTC>0 AND RPAPKPARTC<38) OR RPAPKPARTC>38"

## oma luokka kielletyille väylille (= portaat, terminaalit, selkeät jalankulkualueet)
expression_nogo = "rpastpartc=6 OR rpastpartc=9 OR rpastusety=11 OR rpastusety=14 OR V_LEVEL=3 OR V_LEVEL=8 OR H_LEVEL=6 OR luok_oma=0 OR RPAPKPARTC=38"

# valitaan kevyen liikenteen väylät
arcpy.SelectLayerByAttribute_management(verkosto_lyr, "NEW_SELECTION", expression_kl)
# Annetaan "luokka"-kentälle arvo 2
arcpy.CalculateField_management(verkosto_lyr, luokitus, 2)
# Poistetaan valinta
arcpy.SelectLayerByAttribute_management(verkosto_lyr, "CLEAR_SELECTION")

# valitaan autoliikenteen väylät
arcpy.SelectLayerByAttribute_management(verkosto_lyr, "NEW_SELECTION", expression_auto)
# Annetaan "luokka"-kentälle arvo 1
arcpy.CalculateField_management(verkosto_lyr, luokitus, 1)
# Poistetaan valinta
arcpy.SelectLayerByAttribute_management(verkosto_lyr, "CLEAR_SELECTION")


# valitaan kielletyt väylät
arcpy.SelectLayerByAttribute_management(verkosto_lyr, "NEW_SELECTION", expression_nogo)
# Annetaan "luokka"-kentälle arvo 9
arcpy.CalculateField_management(verkosto_lyr, luokitus, 9)


