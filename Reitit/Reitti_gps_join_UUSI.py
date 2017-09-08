# -*- coding: cp1252 -*-
# Reittitietojen (sisältävät gradientin ja risteystiedot) liittäminen GPS-pisteisiin

import arcpy
import os
from arcpy import env
env.overwriteOutput = True


# Määritetään päähakemisto      
ws_dir = r"[dir_fp]"
# Määritetään reittitiedostojen polut
reitti_ws = os.path.join(ws_dir,"Reitit.gdb")
arcpy.env.workspace = reitti_ws
# Listataan risteystiedot sisältävät reitit
routeList = arcpy.ListFeatureClasses("","","Tieverkkojoin") 
# Listataan workspacesta riippumattomiksi
reittilista = []
for route in routeList:  
    outfp_dir = os.path.join(ws_dir,"Reitit.gdb","Tieverkkojoin") 
    reittilista.append(os.path.join(outfp_dir,route))             


# GPS-pisteiden hakemisto
GPS_fp = os.path.join(ws_dir,"GPS_pisteet.gdb")
arcpy.env.workspace = GPS_fp

# Listataan GPS-pisteet omista dataseteistaan
analyysiList = arcpy.ListFeatureClasses("","","Analyysipisteet")    # analyysipisteet
korvaavatList = arcpy.ListFeatureClasses("","","Korvaavat")         # korvaavat pisteet
lenkkiList = arcpy.ListFeatureClasses("","","Lenkkireitit")         # analysoitujen lenkkireittien pisteet

# Funktio pisteiden täydellisten tiedostopolkujen listaamiseksi
def point_listing(lista, workspace):
    trackList = [] # tehdään datoille workspacesta riippumaton lista
    for track in lista:
        trackList.append(os.path.join(workspace,track))
    return trackList

# Listataan kaikki pisteet tiedostopolkuineen
A_lista = point_listing(analyysiList,os.path.join(GPS_fp,"Analyysipisteet"))
K_lista = point_listing(korvaavatList,os.path.join(GPS_fp,"Korvaavat"))
L_lista = point_listing(lenkkiList,os.path.join(GPS_fp,"Lenkkireitit"))
# Yhdistetään kaikki listat
kaikki_pisteet = A_lista + K_lista + L_lista



# Iteroidaan GPS-pisteiden listaa
for track in kaikki_pisteet[]:                         


    # Määritetään yhdistettävä reittitiedosto         
    routefile = ''
    for route in reittilista:
        name = os.path.basename(route)[1:-6] # poistetaan nimen alusta Z ja lopusta _vayla
        if name in track:
            routefile = route
##    print(track + " ja " + routefile)
    
    # Tehdään Near-analyysi
    arcpy.Near_analysis(track, routefile, "", "NO_LOCATION", "NO_ANGLE", "PLANAR")

    # Joinataan reitit pisteisiin NEAR_FID:n perusteella                                    # lisätään myös Name-kenttä reittitiedostoista (tulee Name_1)                                
    arcpy.JoinField_management(track, "NEAR_FID", routefile, "OBJECTID", ["Total_pituus","Name","Gradientti","Count_lv","Count_auto","Count_kevyt","Rist_yht","TIEE_KUNTA","H_LEVEL","luok_oma","luokka","pyoravayla","Shape_Length"])
                                                                                            

#-----------------------------------------------------------------------------------------------------------------------

