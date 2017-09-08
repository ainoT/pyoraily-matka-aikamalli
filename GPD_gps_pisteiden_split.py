# -*- coding: cp1252 -*-
import os
import geopandas as gpd

# GPS-tiedostojen erottaminen nopeuden, ajan ja et�isyyden kynnysarvoilla

in_folder =r"[filepath]" 


# listaa trackien tiedostopolut
def filepaths(inFolder):
    fullPaths = []
    for root, dirs, files in os.walk(inFolder):
        for filename in files:
            if filename.endswith(".shp"):
                fullpath = os.path.join(root, filename)
                fullPaths.append(fullpath)
    return fullPaths 

files = filepaths(in_folder)

# K�yd��n l�pi shapefilet
for track in files:

    data = gpd.read_file(track)     # luetaan shapefile

    # Luodaan uusi tyhj� kentt� reittiosuudelle
    data['R_part'] = None

    # Reittiosuus-kent�lle annettavalle arvolle oletusarvoksi 1
    idx = 1
    data['R_part'] = idx

    # Iteroidaan rivej�
    for index, row in data.iterrows():
        distance = row['DISTANCE_m']
        speed = row['SPEED_mps']
        time = row['DURATION_s']

        if speed > 20:                          # Jos nopeus > 20 m/s
            data.loc[index,'R_part'] = 999      # annetaan arvoksi 999, GPS on hyppinyt huomattavasti

        # Ehtolause ajalle ja et�isyydelle
        elif time > 300 or distance > 200:      # Jos aika pisteiden v�lill� > 300 s = 5 min, tai et�isyys > 200 m
            idx += 1                            # kasvatetaan idx-muuttujaa yhdell�
            data.loc[index,'R_part'] = idx      # lis�t��n kasvatettu muuttuja R_part kentt��n (reitin osa 1, 2, jne.)
        else:                                   # jos kynnysarvot eiv�t ylity, ei kasvateta idx-muuttujaa
            data.loc[index,'R_part'] = idx      # ja p�ivitet��n "vanha" idx-muuttuja kentt��n
        
          
    ##list(data['R_part'].unique())        


    # Ryhmitell��n data 'R_part'-kent�n mukaan
    grouped = data.groupby('R_part')
        
    # Kirjoitetaan erotellut reitit shapefileiksi
    outFolder = r"[fp]"
    resultFolder = os.path.join(outFolder, 'GPS_split')
    if not os.path.exists(resultFolder):
        os.makedirs(resultFolder)

    # Iteroidaan ryhmitellyt pisteet
    for key, values in grouped:
        count = len(values)             # montako rivi� ryhm�ss� on
        # Muokataan tiedostonime�
        filename = os.path.basename(track)
        outName = filename.replace(".shp","") + "_P%s.shp" % key    # lis�t��n tiedostonimen loppuun reitin osa
        # Luodaan output-fp
        outpath = os.path.join(resultFolder, outName)
        # Ei tallenneta 999 pisteit� JA jos tiedostossa < 20 pistett� niin ei tallenneta!
        if key != 999 and count >= 20:                 
            # Printataan infoa
            print("Processing: %s" % outName)
            # Exportataan reitit
            values.to_file(outpath)

    


