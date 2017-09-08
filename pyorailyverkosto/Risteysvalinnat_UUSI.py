# -*- coding: cp1252 -*-
### Risteysvalintoja ###
import arcpy
from arcpy import env
import os

# Työskentely gdb
wsdir = r"[dir_fp]"
# sallitaan ylikirjoitus
env.overwriteOutput = True


# Luodaan FeatureDataset laskentadatoille
featureDS = "Risteyslaskut"
calcPath = os.path.join(wsdir,featureDS)
sp_ref = r"[fp]"  # Spatial reference

if not arcpy.Exists(calcPath):
    arcpy.CreateFeatureDataset_management(wsdir, featureDS, sp_ref)


# Network Datasetin directory
ND_Dir = os.path.join(wsdir,"Pyoraily_E")
# määritetään workspaceksi
env.workspace = ND_Dir

### Erotetaan ensin todelliset risteykset (junctioniin osuu vähintään 3 tie-elementtiä)
ND_Junctions = "Pyoraily_E_ND_Junctions"
verkosto = "pyorailyverkko_E_tm35fin"
ND_Junc_join = "ND_Junc_join"


# Tehdään spatial join junction-pisteiden ja tieverkon välillä
arcpy.SpatialJoin_analysis(ND_Junctions, verkosto, ND_Junc_join, "JOIN_ONE_TO_ONE", "KEEP_ALL", "", "INTERSECT", "", "")

# Määritetään risteys feature layer, pisteeseen pitää liittyä > 2 tiesegmenttiä jotta se on risteys
Risteys_f = "Risteys_f"
arcpy.MakeFeatureLayer_management(ND_Junc_join, Risteys_f, """Join_Count_1 > 2""", "") # _1 koska tieverkolla on jo yksi Join_Count

# Kopioidaan todelliset risteykset laskentadatasettiin
Risteykset = os.path.join(calcPath,"Risteykset")
arcpy.CopyFeatures_management(Risteys_f, Risteykset)


### Liikennevalotietojen hakeminen
# Haetaan MetropAccess Digiroad 2015:sta DIGIROAD_SEGMENTTI
Segmentti = r"[fp]\MetropAccess_Digiroad_2015.gdb\DIGIROAD_SEGMENTTI"
Liikennevalosegmentti = os.path.join(calcPath,"Liikennevalosegmentti")
# valitaan segmentit joissa DYNTYYPPI = 9  on liikennevalosegmentti
arcpy.Select_analysis(Segmentti, Liikennevalosegmentti, "\"DYN_TYYPPI\" = 9")

# Tehdään Liikennevalosegmenteistä pistemuotoinen:
LVSpoint = os.path.join(calcPath,"LiikennevaloSegmenttiPoint")
arcpy.FeatureToPoint_management(Liikennevalosegmentti, LVSpoint, "CENTROID")
# Tehdään liikennevalopisteistä feature layer
LVpointF = os.path.join(calcPath, "LVpointF")
arcpy.MakeFeatureLayer_management(LVSpoint,LVpointF)


### Haetaan Near-analyysilla 20 m säteellä liikennevalopisteistä olevat risteyspisteet
arcpy.Near_analysis(Risteys_f, LVpointF, "20 Meters", "NO_LOCATION", "NO_ANGLE")

# Tehdään tästä Feature-Layer
LVNJunc_f = "LV_Near_Junctionit_F"
# risteyspiste on 20 m säteellä lv-pisteestä kun NEAR_FID <> -1
arcpy.MakeFeatureLayer_management(Risteys_f, LVNJunc_f, """NEAR_FID <> -1""", "")
# kopioidaan feature classiksi
LVN_out = os.path.join(calcPath,"LV_Near_Junctionit")
arcpy.CopyFeatures_management(LVNJunc_f, LVN_out)


### Valintoja risteyksille

# Tehdään pyöräilyverkostosta vain autotiet sisältävä layer
Verkosto_lyr = "Verkosto_lyr"
arcpy.MakeFeatureLayer_management(verkosto, Verkosto_lyr, "luokka = 1")

# Tehdään select by location potentiaalisten liikennevaloristeysten ja autoteiden välillä
# Oletus että vain auto-tyypin segmenttiin leikkaava risteys voi olla todellinen liikennevaloristeys
arcpy.SelectLayerByLocation_management(LVNJunc_f, "INTERSECT", Verkosto_lyr, "", "NEW_SELECTION")
# Nyt potentiaalisista lv-risteyksistä valittuna vain ne jotka leikkaavat autotiesegmentteihin
# Exportataan liikennevaloristeykset
lv_junc = os.path.join(calcPath,"Liikennevaloristeys")
arcpy.CopyFeatures_management(LVNJunc_f, lv_junc)

# Seuraavaksi valitaan kaikista risteyspisteistä autoteiden kanssa leikkaavat pisteet
# Tehdään select by location risteysten ja autoteiden välillä
arcpy.SelectLayerByLocation_management(Risteys_f, "INTERSECT", Verkosto_lyr, "", "NEW_SELECTION")

# Käännetään valinta, jolloin kaikki kevyen liikenteen risteykset ovat valittuina
arcpy.SelectLayerByLocation_management(Risteys_f, "INTERSECT", Verkosto_lyr, "", "SWITCH_SELECTION")
# Export kevytristeyksille
kevyt_junc = os.path.join(calcPath,"Kevyt_risteys")
arcpy.CopyFeatures_management(Risteys_f, kevyt_junc)

# Vaihdetaan taas valinta jotta saadaan kaikki autoristeykset valittua
arcpy.SelectLayerByLocation_management(Risteys_f, "INTERSECT", Verkosto_lyr, "", "SWITCH_SELECTION")
# Poistetaan valinnasta ne pisteet jotka ovat päällekkäin liikennevaloristeysten kanssa
arcpy.SelectLayerByLocation_management(Risteys_f, "INTERSECT", lv_junc, "", "REMOVE_FROM_SELECTION")
# Nyt valittuna ovat liikennevalottomat autoristeykset
# Exportataan
auto_junc = os.path.join(calcPath,"Autoristeys")
arcpy.CopyFeatures_management(Risteys_f, auto_junc)


