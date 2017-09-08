# -*- coding: cp1252 -*-
# Validointi
# Matka-aikojen laskenta

import arcpy
import os
from arcpy import env
env.overwriteOutput = True

# Määritetään päähakemisto
ws_dir = r"{dir_fp}"
# Reittihakemisto
reitti_fp = os.path.join(ws_dir,"Reitit.gdb")
# Listataan validointireitit
arcpy.env.workspace = reitti_fp
reittilista = arcpy.ListFeatureClasses("","","Validointi")

# GPS-pisteiden hakemisto
GPS_fp = os.path.join(ws_dir,"GPS_pisteet.gdb")
# Valitaan ja listataan GPS-pisteistä niitä vastaavat tallennukset
arcpy.env.workspace = GPS_fp
# Listataan kaikki validointi GPS-pisteet
GPS_lista = arcpy.ListFeatureClasses("","","Validointipisteet")
# Luodaan uusi lista validoinnissa mukana oleville pisteille
validoitavat = []
for track in GPS_lista:
    if "vr_"+track in reittilista:
        validoitavat.append(track)
    

# Lasketaan matka-aika tekemällä summataulu DURATION_s -kentästä
GPS_tbl_fp = os.path.join(ws_dir,"Validointi_GPSajat.gdb")
for points in validoitavat:
    tablename = points
    outtbl = os.path.join(GPS_tbl_fp,tablename)
    statsFields = [["Trackname", "FIRST"],["CycID","FIRST"],["DURATION_s","SUM"],["DISTANCE_m","SUM"],["SPEED_mps","MEAN"]]
    arcpy.Statistics_analysis(points, outtbl, statsFields)
    arcpy.AddField_management(outtbl, "Trackname2", "TEXT")
    arcpy.CalculateField_management(outtbl, "Trackname2", "'"+points+"'", "PYTHON")
    # Ajan summa on sekunteja, lisätään kenttä johon aika lasketaan minuutteina
    arcpy.AddField_management(outtbl, "DURATION_mins", "DOUBLE")
    arcpy.CalculateField_management(outtbl, "DURATION_mins", '!SUM_DURATION_s!/60', "PYTHON")
    

# Listataan GPS-pisteiden summataulut
arcpy.env.workspace = GPS_tbl_fp
GPSsumtables = arcpy.ListTables()
# Yhdistetään ne mergellä
GPStable = "Validointi_GPSsummary"
arcpy.Merge_management(GPSsumtables, GPStable)



# Valitaan tieverkosta select by locationilla kuljettu reitti
tieverkko = r"{fp}"
tieverkko_lyr = "tieverkko_lyr"
arcpy.MakeFeatureLayer_management(tieverkko, "tieverkko_lyr")

arcpy.env.workspace = reitti_fp
for route in reittilista:
    arcpy.SelectLayerByLocation_management(tieverkko_lyr, "HAVE_THEIR_CENTER_IN", route)
    # Tehdään summataulu tieverkon valinnasta
    route_tbl_fp = os.path.join(ws_dir,"Validointi_reittiajat.gdb")
    routename = route.replace("vr_","")
    outsums = os.path.join(route_tbl_fp,routename)
    statsFields2 = [["Aika3", "SUM"],["Aika4","SUM"],["Aika5","SUM"],["Nop3hidaste","MEAN"],["Nop4hidaste","MEAN"],["Nop5hidaste","MEAN"],["Aika3hidaste", "SUM"],["Aika4hidaste", "SUM"],["Aika5hidaste", "SUM"],["Shape_Length","SUM"]]
    arcpy.Statistics_analysis(tieverkko_lyr, outsums, statsFields2)
    arcpy.AddField_management(outsums, "Trackname", "TEXT")
    trackname = "'" + routename + "'"
    arcpy.CalculateField_management(outsums, "Trackname", trackname, "PYTHON")

# Listataan reittien summataulut ja yhdistetään mergellä
arcpy.env.workspace = route_tbl_fp
routesumtables = arcpy.ListTables()
routetable = "Validointi_reittisummary"
arcpy.Merge_management(routesumtables, routetable)


# Join reittinimien perusteella
# Tehdään molemmista tauluista table view
routeview = "routeview"
arcpy.MakeTableView_management(routetable, routeview)
gpsview = "gpsview"
arcpy.MakeTableView_management({tablename}, gpsview)

arcpy.AddJoin_management(routeview, "Trackname", gpsview, "Trackname2", "KEEP_ALL")

# Tallennetaan join omaksi taulukseen
arcpy.CopyRows_management(routeview, "Validointi_summary")


