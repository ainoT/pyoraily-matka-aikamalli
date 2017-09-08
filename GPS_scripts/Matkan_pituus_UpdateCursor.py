# -*- coding: cp1252 -*-

# Reittipisteiden et�isyyksien summaaminen matkan alusta
# Update Cursor

import arcpy
import os

workspace = r"{gdb_fp}"
arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True # Sallitaan ylikirjoitus
#outWorkspace = r"{gdb_fp}" # backup kansio tuloksille

# Listataan workspacessa olevat feature classit
fcList = arcpy.ListFeatureClasses()


# Funktio et�isyysarvojen listaamiseen
def distanceValues(inputfc, field):
    cursor = arcpy.SearchCursor(inputfc)        # SearchCursor iteroi taulukkoa
    distance_values = [0]                       # annetaan listalle ensimm�iseksi arvoksi 0 (koska liikuttu et�isyys on 0)
    cursor.next()                               # siirryt��n seuraavalle riville, jolloin hyp�t��n ensimm�isen rivin null-arvon yli
    for distance in cursor:
        distance_m = distance.getValue(field)   # haetaan yksitt�isen v�lin distance-arvo (alkaen rivilt� 2)
        distance_values.append(distance_m)      # lis�t��n listaan
    return distance_values


# funktio laskee et�isyydet reitin alusta alkaen, summaa ne ja lis�� listaan
def summaa(lista): 
    start_list = []
    summa = 0
    for i in lista:
        summa = i + summa
        start_list.append(summa)
    return start_list


for track in fcList: # k�yd��n l�pi gdb:n sis�lt�m�t feature classit
    dist_lista = distanceValues(track, "DISTANCE_m")    # lista et�isyysarvoista
    dist_summat = summaa(dist_lista)                    # lista et�isyysarvojen summista alusta l�htien
    # lis�t��n kentt� et�isyyssummille
    arcpy.AddField_management(track, "from_start", "FLOAT")
    # Annetaan from_start-kent�lle arvo 0, cursorilla oli vaikeuksia k�sitell� null-arvoja
    arcpy.CalculateField_management(track, "from_start", expression = 0)
    # Luodaan cursor
    with arcpy.da.UpdateCursor(track,["from_start"]) as cursor:
        for row in cursor:
            for i in dist_summat:           # k�yd��n l�pi et�isyyssummien listaa
                row[0] = i                  # annetaan arvoksi listalla seuraavaksi oleva arvo
                cursor.updateRow(row)       # p�ivitet��n rivi
                if row[0]!=dist_summat[-1]: # lopun next pys�ytt�� luupin, menn��n nextiin vain jos ei ole vika arvo
                    cursor.next()           # siirryt��n seuraavalle riville p�ivitt�m��n ettei kaikille tule sama arvo
    #outFeatureClass = os.path.join(outWorkspace, track)     # kopio
    #arcpy.CopyFeatures_management(track, outFeatureClass)   # kopioidaan backup-kansioon
 


