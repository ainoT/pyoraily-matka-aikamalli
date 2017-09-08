# -*- coding: cp1252 -*-

# Reittipisteiden etäisyyksien summaaminen matkan alusta
# Update Cursor

import arcpy
import os

workspace = r"{gdb_fp}"
arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True # Sallitaan ylikirjoitus
#outWorkspace = r"{gdb_fp}" # backup kansio tuloksille

# Listataan workspacessa olevat feature classit
fcList = arcpy.ListFeatureClasses()


# Funktio etäisyysarvojen listaamiseen
def distanceValues(inputfc, field):
    cursor = arcpy.SearchCursor(inputfc)        # SearchCursor iteroi taulukkoa
    distance_values = [0]                       # annetaan listalle ensimmäiseksi arvoksi 0 (koska liikuttu etäisyys on 0)
    cursor.next()                               # siirrytään seuraavalle riville, jolloin hypätään ensimmäisen rivin null-arvon yli
    for distance in cursor:
        distance_m = distance.getValue(field)   # haetaan yksittäisen välin distance-arvo (alkaen riviltä 2)
        distance_values.append(distance_m)      # lisätään listaan
    return distance_values


# funktio laskee etäisyydet reitin alusta alkaen, summaa ne ja lisää listaan
def summaa(lista): 
    start_list = []
    summa = 0
    for i in lista:
        summa = i + summa
        start_list.append(summa)
    return start_list


for track in fcList: # käydään läpi gdb:n sisältämät feature classit
    dist_lista = distanceValues(track, "DISTANCE_m")    # lista etäisyysarvoista
    dist_summat = summaa(dist_lista)                    # lista etäisyysarvojen summista alusta lähtien
    # lisätään kenttä etäisyyssummille
    arcpy.AddField_management(track, "from_start", "FLOAT")
    # Annetaan from_start-kentälle arvo 0, cursorilla oli vaikeuksia käsitellä null-arvoja
    arcpy.CalculateField_management(track, "from_start", expression = 0)
    # Luodaan cursor
    with arcpy.da.UpdateCursor(track,["from_start"]) as cursor:
        for row in cursor:
            for i in dist_summat:           # käydään läpi etäisyyssummien listaa
                row[0] = i                  # annetaan arvoksi listalla seuraavaksi oleva arvo
                cursor.updateRow(row)       # päivitetään rivi
                if row[0]!=dist_summat[-1]: # lopun next pysäyttää luupin, mennään nextiin vain jos ei ole vika arvo
                    cursor.next()           # siirrytään seuraavalle riville päivittämään ettei kaikille tule sama arvo
    #outFeatureClass = os.path.join(outWorkspace, track)     # kopio
    #arcpy.CopyFeatures_management(track, outFeatureClass)   # kopioidaan backup-kansioon
 


