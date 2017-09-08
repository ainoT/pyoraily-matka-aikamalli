# -*- coding: cp1252 -*-
import arcpy
from arcpy import env
import os
import random

# Reittien jako matka- ja lenkkireitteihin

### Haetaan reittipistetiedostot ja listataan ne ###
ws_dir = "[filepath]"
env.workspace = os.path.join(ws_dir,"GPS_pisteet.gdb")
env.overwriteOutput = True

fcList = arcpy.ListFeatureClasses() # listataan tiedostot
trackList = [] # tehdään samoille datoille workspacesta riippumaton lista


for track in fcList: 
    outfp_dir = os.path.join(ws_dir,"GPS_pisteet.gdb")
    trackList.append(os.path.join(outfp_dir,track))             # Lisätään pistetiedostojen polut uuteen listaan

#------------------------------------------------------------------------------------------------------------------------------------    
# Nimet listoille 
ab_lista = []       # tyhjä lista A->B reiteille
lenkkilista = []    # tyhjä lista lenkkimäisille reiteille


# Käydään läpi kaikki tiedostolistalla olevat gps-pistetiedostot

for gps_track in trackList[]:
    print("-----Reitti " + os.path.basename(gps_track)+ "-----")

    ### Trackeista erotetaan ensimmäinen ja viimeinen piste ###
    # http://gis.stackexchange.com/questions/143807/how-to-get-values-of-last-row-in-table-with-arcpy-searchcursor

    a_table = gps_track             # läpikäytävä tiedosto
    order_fld = "Id"                # kenttä jonka mukaan järjestetään tiedot laskevasti
    return_flds = ["Id","from_start","SHAPE@"]   # palautettavat kentät

    sql_clause = (None,'ORDER BY {} DESC'.format(order_fld)) # järjestetään Id:n perusteella laskevasti, niin viimeinen piste on ensimmäinen

    first_row = ''
    last_row = ''
    with arcpy.da.SearchCursor(a_table, return_flds) as cursor: # normaali järjestys
      first_row = cursor.next()

    with arcpy.da.SearchCursor(a_table, return_flds, sql_clause=sql_clause) as cursor: # laskeva järjestys
      last_row = cursor.next()  # last_row

    first_ID = first_row[0]     # tallennetaan ensimmäisen pisteen ID
    last_ID = last_row[0]       # tallennetaan viimeisen pisteen ID
    first_dist = first_row[1]   # ensimmäisen pisteen etäisyystieto
    #print("1. pisteen etäisyystieto: "+ str(first_dist))
    last_dist = last_row[1]     # viimeisen pisteen etäisyystieto
    #print("Viimeisen pisteen etäisyystieto: "+ str(last_dist))
    first_point = first_row[2]  # ensimmäisen pisteen PointGeometry
    last_point = last_row[2]    # viimeisen pisteen PointGeometry

    pt_f = first_point
    pt_l = last_point


    # Lasketaan alku- ja loppupisteiden välinen etäisyys
    tablename = os.path.basename(gps_track)+"_alku_loppu"
    output_table = os.path.join(ws_dir,"GPS_pisteet_kopio.gdb",tablename)
    arcpy.PointDistance_analysis(in_features=pt_f, near_features=pt_l, out_table=output_table)    

    distance_row = ''                                                   # tyhjä muuttuja pisteiden etäisyydelle
    with arcpy.da.SearchCursor(output_table, "DISTANCE") as cursor:     # luetaan cursorin avulla taulukosta
        distance_row = cursor.next()

    point_distance = distance_row[0]                            # tallennetaan etäisyyslukema
    print("Pisteiden välinen etäisyys: " + str(point_distance))

    # Reitin kokonaispituus GPS-pisteistä laskettuna on lopun matkalukema - alun matkalukema
    reittipituus = float(last_dist) - float(first_dist)
    print("Reitin kokonaispituus: " + str(reittipituus))
    
    # Lasketaan alku- ja loppupisteen etäisyyden suhde kokonaismatkaan 
    reittisuhde = point_distance/reittipituus
    print("Pisteiden välinen etäisyys suhteessa kokonaismatkaan: " + str(reittisuhde))
    
    # Jos pisteiden välinen etäisyys > 1/10 koko reitin pituudesta, se on A->B matka
    if reittisuhde > 0.1:
        ab_lista.append(gps_track)
        # Kopioidaan omaan feature datasettiin
##        newname = "AB_" + os.path.basename(gps_track) 
##        outdir = os.path.join(ws_dir,"GPS_pisteet.gdb","A_B_reitit")
##        arcpy.CopyFeatures_management(gps_track, os.path.join(outdir,newname))
    # Jos etäisyys on pienempi, kyseessä on lenkki    
    else:
        lenkkilista.append(gps_track)
        # Kopioidaan omaan feature datasettiin
##        newname = "L_" + os.path.basename(gps_track) 
##        outdir = os.path.join(ws_dir,"GPS_pisteet.gdb","Lenkkireitit")
##        arcpy.CopyFeatures_management(gps_track, os.path.join(outdir,newname))

    # Poistetaan luodut alku- ja loppupisteet ja taulukko
    arcpy.Delete_management(pt_f)
    arcpy.Delete_management(pt_l)
    arcpy.Delete_management(output_table)

    
# Printataan listojen pituudet
print("Reittejä AB-listassa: " + str(len(ab_lista)))
print("Reittejä lenkkilistassa: " + str(len(lenkkilista)))


### Listataan koko aineisto omiin datasetteihin exportatut tiedostot tyypin mukaan
##ab_lista = arcpy.ListFeatureClasses("","","A_B_reitit")
##lenkkilista = arcpy.ListFeatureClasses("","","Lenkkireitit")


# Tehdään lista kunkin henkilön AB-reiteille
ab_lista2 = []
ab_lista3 = []
ab_lista4 = []
ab_lista5 = []
ab_lista6 = []
ab_lista7 = []
ab_lista8 = []
ab_lista9 = []
ab_lista10 = []
ab_lista11 = []
ab_lista12 = []
ab_lista13 = [] 
ab_lista14 = [] 
ab_lista15 = []
ab_lista16 = []
ab_lista17 = []
ab_lista18 = []
ab_lista19 = []
ab_lista20 = []
ab_lista21 = [] 
ab_lista22 = []
ab_lista23 = []
ab_lista24 = []
ab_lista25 = []
ab_lista26 = []
ab_lista27 = []
ab_lista28 = []
ab_lista30 = []
ab_lista32 = []
ab_lista33 = []
ab_lista34 = []
ab_lista35 = []
ab_lista36 = []
ab_lista37 = []
ab_lista39 = []
ab_lista40 = []
ab_lista43 = []
ab_lista44 = []
ab_lista45 = []
ab_lista46 = []
ab_lista47 = []
ab_lista48 = []
ab_lista49 = []
ab_lista50 = []

# Lisätään hlökohtaiseen listaan jos AB-reittejä on
for track in ab_lista:
    if "C02_" in track:
        ab_lista2.append(track)
    elif "C3_" in track:
        ab_lista3.append(track)
    elif "C04_" in track:
        ab_lista4.append(track)
    elif "C05_" in track:
        ab_lista5.append(track)
    elif "C06_" in track:
        ab_lista6.append(track)
    elif "C07_" in track:
        ab_lista7.append(track)
    elif "C08_" in track:
        ab_lista8.append(track)
    elif "C09_" in track:
        ab_lista9.append(track)
    elif "C10_" in track:
        ab_lista10.append(track)
    elif "C11_" in track:
        ab_lista11.append(track)
    elif "C12_" in track:
        ab_lista12.append(track)
    elif "C13_" in track:
        ab_lista13.append(track)
    elif "C14_" in track:
        ab_lista14.append(track)
    elif "C15_" in track:
        ab_lista15.append(track)
    elif "C16_" in track:
        ab_lista16.append(track)
    elif "C17_" in track:
        ab_lista17.append(track)
    elif "C18_" in track:
        ab_lista18.append(track)
    elif "C19_" in track:
        ab_lista19.append(track)
    elif "C20_" in track:
        ab_lista20.append(track)
    elif "C21_" in track:
        ab_lista21.append(track)   
    elif "C22_" in track:
        ab_lista22.append(track)
    elif "C23_" in track:
        ab_lista23.append(track)
    elif "C24_" in track:
        ab_lista24.append(track)
    elif "C25_" in track:
        ab_lista25.append(track)
    elif "C26_" in track:
        ab_lista26.append(track)
    elif "C27_" in track:
        ab_lista27.append(track)
    elif "C28_" in track:
        ab_lista28.append(track)
    elif "C30_" in track:
        ab_lista30.append(track)
    elif "C32_" in track:
        ab_lista32.append(track)
    elif "C33_" in track:
        ab_lista33.append(track)
    elif "C34_" in track:
        ab_lista34.append(track)
    elif "C35_" in track:
        ab_lista35.append(track)
    elif "C36_" in track:
        ab_lista36.append(track)
    elif "C37_" in track:
        ab_lista37.append(track)
    elif "C39_" in track:
        ab_lista39.append(track)
    elif "C40_" in track:
        ab_lista40.append(track)
    elif "C43_" in track:
        ab_lista43.append(track)
    elif "C44_" in track:
        ab_lista44.append(track)
    elif "C45_" in track:
        ab_lista45.append(track)
    elif "C46_" in track:
        ab_lista46.append(track)
    elif "C47_" in track:
        ab_lista47.append(track)
    elif "C48_" in track:
        ab_lista48.append(track)
    elif "C49_" in track:
        ab_lista49.append(track)
    elif "C50_" in track:
        ab_lista50.append(track)

# Tehdään henkilökohtainen lenkkilista
l_lista2 = []
l_lista3 = []
l_lista4 = []
l_lista5 = []
l_lista6 = [] 
l_lista7 = []
l_lista8 = []
l_lista9 = []
l_lista10 = []
l_lista11 = []
l_lista12 = []
l_lista13 = [] 
l_lista14 = [] 
l_lista15 = []
l_lista16 = []
l_lista17 = []
l_lista18 = []
l_lista19 = []
l_lista20 = []
l_lista21 = [] 
l_lista22 = []
l_lista23 = []
l_lista24 = []
l_lista25 = []
l_lista26 = []
l_lista27 = []
l_lista28 = []
l_lista30 = []
l_lista32 = []
l_lista33 = []
l_lista34 = []
l_lista35 = []
l_lista36 = []
l_lista37 = []
l_lista39 = []
l_lista40 = []
l_lista43 = []
l_lista44 = []
l_lista45 = []
l_lista46 = []
l_lista47 = []
l_lista48 = []
l_lista49 = []
l_lista50 = []

# Lisätään hlökohtaiseen listaan jos lenkkireittejä on
for track in lenkkilista:
    if "C02_" in track:
        l_lista2.append(track)
    elif "C3_" in track:
        l_lista3.append(track)
    elif "C04_" in track:
        l_lista4.append(track)
    elif "C05_" in track:
        l_lista5.append(track)
    elif "C06_" in track:
        l_lista6.append(track)
    elif "C07_" in track:
        l_lista7.append(track)
    elif "C08_" in track:
        l_lista8.append(track)
    elif "C09_" in track:
        l_lista9.append(track)
    elif "C10_" in track:
        l_lista10.append(track)
    elif "C11_" in track:
        l_lista11.append(track)
    elif "C12_" in track:
        l_lista12.append(track)
    elif "C13_" in track:
        l_lista13.append(track)
    elif "C14_" in track:
        l_lista14.append(track)
    elif "C15_" in track:
        l_lista15.append(track)
    elif "C16_" in track:
        l_lista16.append(track)
    elif "C17_" in track:
        l_lista17.append(track)
    elif "C18_" in track:
        l_lista18.append(track)
    elif "C19_" in track:
        l_lista19.append(track)
    elif "C20_" in track:
        l_lista20.append(track)
    elif "C21_" in track:
        l_lista21.append(track)   
    elif "C22_" in track:
        l_lista22.append(track)
    elif "C23_" in track:
        l_lista23.append(track)
    elif "C24_" in track:
        l_lista24.append(track)
    elif "C25_" in track:
        l_lista25.append(track)
    elif "C26_" in track:
        l_lista26.append(track)
    elif "C27_" in track:
        l_lista27.append(track)
    elif "C28_" in track:
        l_lista28.append(track)
    elif "C30_" in track:
        l_lista30.append(track)
    elif "C32_" in track:
        l_lista32.append(track)
    elif "C33_" in track:
        l_lista33.append(track)
    elif "C34_" in track:
        l_lista34.append(track)
    elif "C35_" in track:
        l_lista35.append(track)
    elif "C36_" in track:
        l_lista36.append(track)
    elif "C37_" in track:
        l_lista37.append(track)
    elif "C39_" in track:
        l_lista39.append(track)
    elif "C40_" in track:
        l_lista40.append(track)
    elif "C43_" in track:
        l_lista43.append(track)
    elif "C44_" in track:
        l_lista44.append(track)
    elif "C45_" in track:
        l_lista45.append(track)
    elif "C46_" in track:
        l_lista46.append(track)
    elif "C47_" in track:
        l_lista47.append(track)
    elif "C48_" in track:
        l_lista48.append(track)
    elif "C49_" in track:
        l_lista49.append(track)
    elif "C50_" in track:
        l_lista50.append(track)



# Printataan kaikki tulokset
print("02 A->B reittejä "+str(len(ab_lista2))+" kpl")
print("02 lenkkireittejä "+str(len(l_lista2))+" kpl")
print("3 A->B reittejä "+str(len(ab_lista3))+" kpl")
print("3 lenkkireittejä "+str(len(l_lista3))+" kpl")
print("04 A->B reittejä "+str(len(ab_lista4))+" kpl")
print("04 lenkkireittejä "+str(len(l_lista4))+" kpl")
print("05 A->B reittejä "+str(len(ab_lista5))+" kpl")
print("05 lenkkireittejä "+str(len(l_lista5))+" kpl")
print("06 A->B reittejä "+str(len(ab_lista6))+" kpl")
print("06 lenkkireittejä "+str(len(l_lista6))+" kpl")
print("07 A->B reittejä "+str(len(ab_lista7))+" kpl")
print("07 lenkkireittejä "+str(len(l_lista7))+" kpl")
print("08 A->B reittejä "+str(len(ab_lista8))+" kpl")
print("08 lenkkireittejä "+str(len(l_lista8))+" kpl")
print("09 A->B reittejä "+str(len(ab_lista9))+" kpl")
print("09 lenkkireittejä "+str(len(l_lista9))+" kpl")
print("10 A->B reittejä "+str(len(ab_lista10))+" kpl")
print("10 lenkkireittejä "+str(len(l_lista10))+" kpl")
print("11 A->B reittejä "+str(len(ab_lista11))+" kpl")
print("11 lenkkireittejä "+str(len(l_lista11))+" kpl")
print("12 A->B reittejä "+str(len(ab_lista12))+" kpl")
print("12 lenkkireittejä "+str(len(l_lista12))+" kpl")
print("13 A->B reittejä "+str(len(ab_lista13))+" kpl")
print("13 lenkkireittejä "+str(len(l_lista13))+" kpl")
print("14 A->B reittejä "+str(len(ab_lista14))+" kpl")
print("14 lenkkireittejä "+str(len(l_lista14))+" kpl")
print("15 A->B reittejä "+str(len(ab_lista15))+" kpl")
print("15 lenkkireittejä "+str(len(l_lista15))+" kpl")
print("16 A->B reittejä "+str(len(ab_lista16))+" kpl")
print("16 lenkkireittejä "+str(len(l_lista16))+" kpl")
print("17 A->B reittejä "+str(len(ab_lista17))+" kpl")
print("17 lenkkireittejä "+str(len(l_lista17))+" kpl")
print("18 A->B reittejä "+str(len(ab_lista18))+" kpl")
print("18 lenkkireittejä "+str(len(l_lista18))+" kpl")
print("19 A->B reittejä "+str(len(ab_lista19))+" kpl")
print("19 lenkkireittejä "+str(len(l_lista19))+" kpl")
print("20 A->B reittejä "+str(len(ab_lista20))+" kpl")
print("20 lenkkireittejä "+str(len(l_lista20))+" kpl")
print("21 A->B reittejä "+str(len(ab_lista21))+" kpl")
print("21 lenkkireittejä "+str(len(l_lista21))+" kpl")
print("22 A->B reittejä "+str(len(ab_lista22))+" kpl")
print("22 lenkkireittejä "+str(len(l_lista22))+" kpl")
print("23 A->B reittejä "+str(len(ab_lista23))+" kpl")
print("23 lenkkireittejä "+str(len(l_lista23))+" kpl")
print("24 A->B reittejä "+str(len(ab_lista24))+" kpl")
print("24 lenkkireittejä "+str(len(l_lista24))+" kpl")
print("25 A->B reittejä "+str(len(ab_lista25))+" kpl")
print("25 lenkkireittejä "+str(len(l_lista25))+" kpl")
print("26 A->B reittejä "+str(len(ab_lista26))+" kpl")
print("26 lenkkireittejä "+str(len(l_lista26))+" kpl")
print("27 A->B reittejä "+str(len(ab_lista27))+" kpl")
print("27 lenkkireittejä "+str(len(l_lista27))+" kpl")
print("28 A->B reittejä "+str(len(ab_lista28))+" kpl")
print("28 lenkkireittejä "+str(len(l_lista28))+" kpl")
print("30 A->B reittejä "+str(len(ab_lista30))+" kpl")
print("30 lenkkireittejä "+str(len(l_lista30))+" kpl")
print("32 A->B reittejä "+str(len(ab_lista32))+" kpl")
print("32 lenkkireittejä "+str(len(l_lista32))+" kpl")
print("33 A->B reittejä "+str(len(ab_lista33))+" kpl")
print("33 lenkkireittejä "+str(len(l_lista33))+" kpl")
print("34 A->B reittejä "+str(len(ab_lista34))+" kpl")
print("34 lenkkireittejä "+str(len(l_lista34))+" kpl")
print("35 A->B reittejä "+str(len(ab_lista35))+" kpl")
print("35 lenkkireittejä "+str(len(l_lista35))+" kpl")
print("36 A->B reittejä "+str(len(ab_lista36))+" kpl")
print("36 lenkkireittejä "+str(len(l_lista36))+" kpl")
print("37 A->B reittejä "+str(len(ab_lista37))+" kpl")
print("37 lenkkireittejä "+str(len(l_lista37))+" kpl")
print("39 A->B reittejä "+str(len(ab_lista39))+" kpl")
print("39 lenkkireittejä "+str(len(l_lista39))+" kpl")
print("40 A->B reittejä "+str(len(ab_lista40))+" kpl")
print("40 lenkkireittejä "+str(len(l_lista40))+" kpl")
print("43 A->B reittejä "+str(len(ab_lista43))+" kpl")
print("43 lenkkireittejä "+str(len(l_lista43))+" kpl")
print("44 A->B reittejä "+str(len(ab_lista44))+" kpl")
print("44 lenkkireittejä "+str(len(l_lista44))+" kpl")
print("45 A->B reittejä "+str(len(ab_lista45))+" kpl")
print("45 lenkkireittejä "+str(len(l_lista45))+" kpl")
print("46 A->B reittejä "+str(len(ab_lista46))+" kpl")
print("46 lenkkireittejä "+str(len(l_lista46))+" kpl")
print("47 A->B reittejä "+str(len(ab_lista47))+" kpl")
print("47 lenkkireittejä "+str(len(l_lista47))+" kpl")
print("48 A->B reittejä "+str(len(ab_lista48))+" kpl")
print("48 lenkkireittejä "+str(len(l_lista48))+" kpl")
print("49 A->B reittejä "+str(len(ab_lista49))+" kpl")
print("49 lenkkireittejä "+str(len(l_lista49))+" kpl")
print("50 A->B reittejä "+str(len(ab_lista50))+" kpl")
print("50 lenkkireittejä "+str(len(l_lista50))+" kpl")


# Määritetään output-datasetit
analyysiDS = "Analyysipisteet"
AnalyysiPath = os.path.join(ws_dir, "GPS_pisteet.gdb", analyysiDS)

validointiDS = "Validointipisteet"
ValidPath = os.path.join(ws_dir, "GPS_pisteet.gdb", validointiDS)

# Funktio listojen läpikäyntiin
def listacheck(ABlista,Llista):
        print("Prosessoidaan " + str(ABlista[0]) + " listaa")
        # jos AB-listaa alle 100
        if len(ABlista) <= 100:
            for x in ABlista:
                newname = "A" + os.path.basename(x) 
                analysis_point = os.path.join(AnalyysiPath,newname)
                # kopioidaan Analyysi DS:iin
                print("AB reitteja <100, kopioidaan analyysiin " + newname)
                arcpy.CopyFeatures_management(x, analysis_point)

            # Jos lenkkilistalla on jotain, kopioidaan Lenkkireitit-datasettiin
            if len(Llista) > 0:
                for lenkki in Llista:
                    newname_L = "L_" + os.path.basename(lenkki) 
                    outdir = os.path.join(ws_dir,"GPS_pisteet.gdb","Lenkkireitit")
                    print("Kopioidaan lenkkireitti " + newname_L)
                    arcpy.CopyFeatures_management(lenkki, os.path.join(outdir,newname_L))

            
        # jos AB-listalla yli 100, tee seuraavaa ja lenkkilistalle ei tarvitse tehdä mitään
        else:
            print("Yli 100 AB reittia")
            # Tarkistetaan montako AB-reittiä
            montako = int(len(ABlista))
            # lasketaan montako reittiä yli sadan
            yli_sadan = montako - 100
            # jos extraa alle 120
            if yli_sadan < 100:
                # valitaan satunnaisesti 100 + loput
                valitaan = 100 + yli_sadan
            # jos enemmän, valitaan 200
            else:
                valitaan = 200
            print("Valitaan satunnaisesti: " + str(valitaan))

            # Valitaan satunnaiset 200 pistetiedostoa (100 analyysiin, 100 validointiin)
            # random.sample http://stackoverflow.com/questions/15511349/select-50-items-from-list-at-random-to-write-to-file
            randomList = random.sample(ABlista,valitaan)

            # Koska pisteet on valittu satunnaisessa järjestyksessä
            # Luupataan 100 ensimmäistä
            for z in randomList[0:100]:
                newname1 = "A" + os.path.basename(z)
                analysis_point = os.path.join(AnalyysiPath,newname1)
                # kopioidaan Analyysi DS:iin
                print("Kopioidaan analyysiin: " + newname1)
                arcpy.CopyFeatures_management(z, analysis_point)

            # Luupataan loput
            for y in randomList[100:]:
                newname2 = "V" + os.path.basename(y)
                val_point = os.path.join(ValidPath,newname2)
                # kopioidaan Validointi DS:iin
                print("Kopioidaan validointiin: " + newname2)
                arcpy.CopyFeatures_management(y, val_point)	

# Kutstutaan funktio
listacheck(ab_lista17,l_lista17)
listacheck(ab_lista18,l_lista18)
listacheck(ab_lista19,l_lista19)
listacheck(ab_lista20,l_lista20)
listacheck(ab_lista21,l_lista21)
listacheck(ab_lista22,l_lista22)
listacheck(ab_lista23,l_lista23)
listacheck(ab_lista24,l_lista24)
listacheck(ab_lista25,l_lista25)
listacheck(ab_lista26,l_lista26)
listacheck(ab_lista27,l_lista27)
listacheck(ab_lista28,l_lista28)
listacheck(ab_lista30,l_lista30)
listacheck(ab_lista32,l_lista32)
listacheck(ab_lista33,l_lista33)
listacheck(ab_lista34,l_lista34)
listacheck(ab_lista35,l_lista35)
listacheck(ab_lista36,l_lista36)
listacheck(ab_lista37,l_lista37)
listacheck(ab_lista39,l_lista39)
listacheck(ab_lista40,l_lista40)
listacheck(ab_lista43,l_lista43)
listacheck(ab_lista44,l_lista44)
listacheck(ab_lista45,l_lista45)
listacheck(ab_lista46,l_lista46)
listacheck(ab_lista47,l_lista47)
listacheck(ab_lista48,l_lista48)
listacheck(ab_lista49,l_lista49)
listacheck(ab_lista50,l_lista50)

