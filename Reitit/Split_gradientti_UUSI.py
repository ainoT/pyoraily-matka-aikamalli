# -*- coding: cp1252 -*-
# Reittien jakaminen osiin gradientin laskemista varten
# Vaihtoehto 2 
# https://arcpy.wordpress.com/2014/10/30/split-into-equal-length-features/

import arcpy
import os

        
# M��ritet��n workspace      
workspace = r"[gdb_fp]"
arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True # Sallitaan ylikirjoitus
# Listataan Reitit.gdb:ssa olevat reitit
fcList = arcpy.ListFeatureClasses()

# Luodaan feature dataset segmentoituja reittej� varten
segmentDS = "Segmentoidut_reitit" 
sp_ref = r"[fp]"

if not arcpy.Exists(segmentDS):
    arcpy.CreateFeatureDataset_management(workspace, segmentDS, sp_ref)

out_segDS = os.path.join(workspace, segmentDS) # Polku Feature Datasettiin

# Reittien l�pik�ynti listasta
for reitti in fcList:                                                         
    in_feature = reitti
    out_name = reitti.replace("reitti","Split") # Poistetaan outputin nimest� 'reitti', laitetaan tilalle split
    out_feature = os.path.join(out_segDS, out_name)
    line = arcpy.da.SearchCursor(in_feature, ("SHAPE@",)).next()[0]
    out_count = int(line.length/50) # lasketaan kuinka moneen osaan reitti pit�� jakaa jakamalla sen pituus 50 metrill�
    # Jaetaan reitti out_countin mukaisesti osiin jotka ovat n. 50 m pitki�
    arcpy.CopyFeatures_management([line.segmentAlongLine(i/float(out_count), ((i+1)/float(out_count)), True) for i in range(0, out_count)], out_feature)
    # Lis�t��n kentt� reitin kokonaispituudelle
    arcpy.AddField_management(out_feature, 'Total_pituus', 'DOUBLE')
    # Lasketaan kokonaispituus
    arcpy.CalculateField_management(out_feature, 'Total_pituus', line.length)

### Korkeustiedon lis��minen ###
# http://gis.stackexchange.com/questions/165683/how-do-i-find-the-slope-of-road-segments-with-point-elevation-data-of-the-same-l

# Listataan segmentoidut reitit 
segmentList = arcpy.ListFeatureClasses("","", "Segmentoidut_reitit")

# Luodaan uusi feature dataset 3D-reittej� varten
DS_3D = "reitit_3D"
if not arcpy.Exists(DS_3D):
    arcpy.CreateFeatureDataset_management(workspace, DS_3D, sp_ref)

path_3D = os.path.join(workspace, DS_3D) # Polku 3D-Datasettiin

# Interpolate shape: http://pro.arcgis.com/en/pro-app/tool-reference/3d-analyst/interpolate-shape.htm

# Tarkistetaan lisenssi
arcpy.CheckOutExtension("3D")

# Korkeusmalli
surface = r"[fp]"

# K�yd��n l�pi segmentoidut reitit
for fc in segmentList:
    if "Split_AC" in fc:                    # vaihdetaan ja yhten�istet��n nimet
        newname = fc.replace("Split_A","Z")
    elif "Split_LC" in fc:
        newname = fc.replace("Split_L","Z")
    outFC = os.path.join(path_3D,newname)   # output feature class
    method = "BILINEAR"
    # InterpolateShape
    arcpy.InterpolateShape_3d(surface, fc, outFC, "", 1, method)
    # Lis�t��n kentt� reitin nimelle
    arcpy.AddField_management(outFC, "Name", "STRING")
    # Lis�t��n kentt� gradientin laskemiseksi
    arcpy.AddField_management(outFC, "Gradientti", "DOUBLE")
    # Lis�t��n nimi
    name = "'" + newname + "'"
    arcpy.CalculateField_management(outFC, "Name", name, "PYTHON_9.3")
    # Lasketaan gradientti lausekkeen avulla
    expression = "(!Shape!.lastPoint.Z- !Shape!.firstPoint.Z)/ !Shape!.length*100"
    arcpy.CalculateField_management(outFC, "Gradientti", expression, "PYTHON_9.3")
    # Poistetaan pelkk� splitattu reitti
    arcpy.Delete_management(fc)




