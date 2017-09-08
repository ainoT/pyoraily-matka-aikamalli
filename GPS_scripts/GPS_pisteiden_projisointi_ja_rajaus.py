# -*- coding: cp1252 -*-
# GPS-pisteiden projisointi

import arcpy
import os
from arcpy import env
arcpy.env.overwriteOutput = True

input_fp = r"[gps_fp]"


# listaa trackit
def filepaths(inFolder):
    fullPaths = []
    for root, dirs, files in os.walk(inFolder):
        for filename in files:
            if filename.endswith(".shp"):
                fullpath = os.path.join(root, filename)
                fullPaths.append(fullpath)
    return fullPaths 

files = filepaths(input_fp)

verkosto = r"[fp]"
spatial_ref = arcpy.Describe(verkosto).spatialReference # tallennetaan verkoston koordinaatisto spatial_ref-muuttujaan

# Polku output-kansioon
out_folder = r"[dir_fp]"
if not os.path.exists(out_folder):      # luodaan kansio jos ei ole olemassa
    os.makedirs(out_folder)



# Projisoidaan gps-pisteet EUREF-FIN TM35FIN -koordinaatistoon (EPSG:3067)
for shape in files:
    filename = os.path.basename(shape)
    newname = "C" + filename                    # myöhemmissä gdb-vaiheissa nimi ei voi alkaa numerolla, siksi lisätään C alkuun jo nyt
    out_shp = os.path.join(out_folder,newname)
    
    # Tehdään pistetidostosta layer jotta voidaan laskea pisteiden lukumäärä                                ### EI OLISI VÄLTTÄMÄTÖNTÄ TEHDÄ LYRIA
    lyrname = filename.replace(".shp","")
    lyr = arcpy.MakeFeatureLayer_management(shape, os.path.join(input_fp,lyrname))  # tehdään lyrit lähtökansioon
    # Haetaan pisteiden määrä
    if arcpy.GetCount_management(lyr).getOutput(0) >= 20:                           # jos pisteitä on vähintään 20, projisoidaan tuloskansioon
        arcpy.Project_management(shape, out_shp, spatial_ref, "EUREF_FIN_To_WGS_1984")
    else:
        print("Tiedostossa "+filename+" alle 20 pistetta")

##    # Poistetaan alkuperäinen wgs84-shape 
##    arcpy.Delete_management(shape)



# Rajaus pk-seudulle (clip)

pk_rajat = r"[fp]"
clip_folder = r"[dir_fp]"
if not os.path.exists(clip_folder):      # luodaan kansio jos ei ole olemassa
    os.makedirs(clip_folder)

# Listataan tiedostot projisoitujen kansiosta    
gps_list = filepaths(out_folder)

for x in gps_list:
    f_name = os.path.basename(x)
    gps_clipped = os.path.join(clip_folder,f_name)
    
    # Katsotaan select by locationilla ovatko pisteet tutkimusaluebufferin sisällä
    # GPS shapefileista layerit jotta voi tehdä select by locationin
    lyrname = f_name.replace(".shp","")
    lyr = arcpy.MakeFeatureLayer_management(x, os.path.join(out_folder,lyrname))
    # Rajataan pisteet tutkimusalueelle pk-seutu-polygonin avulla
    in_area = arcpy.SelectLayerByLocation_management(lyr,"WITHIN",pk_rajat,"","NEW_SELECTION")
    
    # Tarkistetaan ovatko pisteet tutkimusalueella
    if int(arcpy.GetCount_management(in_area).getOutput(0)) >= 20:          # Jos polygonin sisällä on vähintään 20 pistettä,
        out_area = arcpy.SelectLayerByLocation_management(lyr,"WITHIN",pk_rajat,"","SWITCH_SELECTION") # käännetään valinta ja tarkistetaan onko niitä myös ulkopuolella
        if int(arcpy.GetCount_management(out_area).getOutput(0)) > 0:       # Jos ulkopuolella on pisteitä,
            arcpy.SelectLayerByAttribute_management(lyr, "CLEAR_SELECTION") # poistetaan kaikki valinnat (onko välttämättä tarpeen?)
            arcpy.Clip_analysis(x, pk_rajat, gps_clipped)                   # clipataan gps-tiedosto pk-polygonilla
        else:
            arcpy.SelectLayerByAttribute_management(lyr, "CLEAR_SELECTION") # poistetaan kaikki valinnat (onko välttämättä tarpeen?)
            arcpy.CopyFeatures_management(x, gps_clipped)                   # Jos ulkopuolella ei ole pisteitä, kopioidaan alkup. tiedosto sellaisenaan kohdekansioon
    else:                                                                   # Jos ei ole yhtään pisteitä tutkimusalueen sisällä,
        print(f_name + " tutkimusalueen ulkopuolella, poistuu")             # tulostetaan jatkoanalyysista pois jäävän tiedoston nimi (tiedosto jää vanhaan kansioon, ei siirretä uuteen)
    

