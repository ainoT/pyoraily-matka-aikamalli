# -*- coding: cp1252 -*-
# Risteystietojen liittäminen gradientti-tiedon sisältäviin reitteihin

import arcpy
import os

# Määritetään workspace      
wspace = r"[dir_fp]"
reitti_ws = os.path.join(wspace,"Reitit.gdb")
arcpy.env.workspace = reitti_ws
arcpy.env.overwriteOutput = True # Sallitaan ylikirjoitus
# Listataan 3D-reitit
routeList = arcpy.ListFeatureClasses("","","reitit_3D")
        
# Luodaan feature dataset reittien ja risteystietojen yhdistelmälle
risteysjoinDS = "Risteysjoin" 
sp_ref = "fp" # tiedosto josta haetaan spatiaalinen referenssi

if not arcpy.Exists(risteysjoinDS):
    arcpy.CreateFeatureDataset_management(reitti_ws, risteysjoinDS, sp_ref)

join_fp = os.path.join(reitti_ws, risteysjoinDS) # Polku Feature Datasettiin


# Polut liikennevalo-, auto- ja kevyenliikenteen risteyksiin
lv_risteys = r"[out_fp]"
autoristeys = r"[out_fp]"
kevytristeys = r"[out_fp]"

# Iteroidaan reittilistaa
for route in routeList:                         

    # Lisätään kentät pyöräilijän ID:lle 
    arcpy.AddField_management(route,"CycID", "SHORT")
    namesplit = route.split("_")                                            # erotetaan pyöräiljän ID-numero
    numsplit = namesplit[0].split("C")
    ID_expression = numsplit[1]
    arcpy.CalculateField_management(route, "CycID", int(ID_expression))     # lisätään CycID-numero integerina

    
    # Liikennevaloristeysten liittäminen #
    # Luodaan nimi ja polku tiedostolle johon liitetään liikennevaloristeykset
    lv_join = route + "_lv"
    lv_out = os.path.join(join_fp,lv_join)
    
    # Fieldmappings siirrettävien tietojen valitsemiseksi
    # http://pro.arcgis.com/en/pro-app/tool-reference/analysis/spatial-join.htm

    fieldmappings = arcpy.FieldMappings()
    fieldmappings.addTable(route)
    fieldmappings.addTable(lv_risteys)
 
    # Haetaan sailytettava kenttä, esim. Name
    sailytettava = fieldmappings.findFieldMapIndex("Join_Count")
    fieldmap = fieldmappings.getFieldMap(sailytettava)
     
    # Get the output field's properties as a field object
    field = fieldmap.outputField
     
    # Rename the field and pass the updated field object back into the field map
    field.name = "Count_lv"
    field.aliasName = "Count_lv"
    fieldmap.outputField = field
     
    # Set the merge rule and then replace the old fieldmap in the mappings object with the updated one
    fieldmap.mergeRule = "count"
    fieldmappings.replaceFieldMap(sailytettava, fieldmap)
     
    # Delete fields that are no longer applicable           ### Poistettavista voisi tehdä listan!       
    x2 = fieldmappings.findFieldMapIndex("TARGET_FID")
    fieldmappings.removeFieldMap(x2)
    x3 = fieldmappings.findFieldMapIndex("Join_Count_1")
    fieldmappings.removeFieldMap(x3)
    x4 = fieldmappings.findFieldMapIndex("TARGET_FID_1")
    fieldmappings.removeFieldMap(x4)
    x5 = fieldmappings.findFieldMapIndex("KLEROTYP")
    fieldmappings.removeFieldMap(x5)
    x6 = fieldmappings.findFieldMapIndex("PANIMI_FIN")
    fieldmappings.removeFieldMap(x6)
    x7 = fieldmappings.findFieldMapIndex("TIEE_TILA")
    fieldmappings.removeFieldMap(x7)
    x8 = fieldmappings.findFieldMapIndex("VAYLATYYPP")
    fieldmappings.removeFieldMap(x8)
    x9 = fieldmappings.findFieldMapIndex("TOIMINNALL")
    fieldmappings.removeFieldMap(x9)
    x10 = fieldmappings.findFieldMapIndex("TYYPPI")
    fieldmappings.removeFieldMap(x10)
    x11 = fieldmappings.findFieldMapIndex("LIIKENNEVI")
    fieldmappings.removeFieldMap(x11)
    x12 = fieldmappings.findFieldMapIndex("INV_PAALU_")
    fieldmappings.removeFieldMap(x12)
    x13 = fieldmappings.findFieldMapIndex("INV_PAAL_1")
    fieldmappings.removeFieldMap(x13)
    x14 = fieldmappings.findFieldMapIndex("VIITE_OID")
    fieldmappings.removeFieldMap(x14)
    x15 = fieldmappings.findFieldMapIndex("PAALLYSTE")
    fieldmappings.removeFieldMap(x15)
    x16 = fieldmappings.findFieldMapIndex("SILTATAITU")
    fieldmappings.removeFieldMap(x16)
    x17 = fieldmappings.findFieldMapIndex("DOCNAME")
    fieldmappings.removeFieldMap(x17)
    x18 = fieldmappings.findFieldMapIndex("Laji")
    fieldmappings.removeFieldMap(x18)
    x19 = fieldmappings.findFieldMapIndex("Lajin_seli")
    fieldmappings.removeFieldMap(x19)
    x20 = fieldmappings.findFieldMapIndex("Z1")
    fieldmappings.removeFieldMap(x20)
    x21 = fieldmappings.findFieldMapIndex("Z2")
    fieldmappings.removeFieldMap(x21)
    x22 = fieldmappings.findFieldMapIndex("rpastpartc")
    fieldmappings.removeFieldMap(x22)
    x23 = fieldmappings.findFieldMapIndex("rpastusety")
    fieldmappings.removeFieldMap(x23)
    x24 = fieldmappings.findFieldMapIndex("rpaststatu")
    fieldmappings.removeFieldMap(x24)
    x25 = fieldmappings.findFieldMapIndex("RPASTPAVIN")
    fieldmappings.removeFieldMap(x25)
    x26 = fieldmappings.findFieldMapIndex("V_LEVEL")
    fieldmappings.removeFieldMap(x26)
    x27 = fieldmappings.findFieldMapIndex("RPAPKPARTC")
    fieldmappings.removeFieldMap(x27)
    x28 = fieldmappings.findFieldMapIndex("RPAPKUSETY")
    fieldmappings.removeFieldMap(x28)
    x29 = fieldmappings.findFieldMapIndex("RPAPKPAVIN")
    fieldmappings.removeFieldMap(x29)
    x30 = fieldmappings.findFieldMapIndex("Pituus")
    fieldmappings.removeFieldMap(x30)
    x31 = fieldmappings.findFieldMapIndex("NEAR_FID")
    fieldmappings.removeFieldMap(x31)
    x32 = fieldmappings.findFieldMapIndex("NEAR_DIST")
    fieldmappings.removeFieldMap(x32)
    x33 = fieldmappings.findFieldMapIndex("FID_")
    fieldmappings.removeFieldMap(x33)
    x34 = fieldmappings.findFieldMapIndex("TIEE_KUNTA")
    fieldmappings.removeFieldMap(x34)
    x35 = fieldmappings.findFieldMapIndex("H_LEVEL")
    fieldmappings.removeFieldMap(x35)
    x36 = fieldmappings.findFieldMapIndex("luok_oma")
    fieldmappings.removeFieldMap(x36)
    x37 = fieldmappings.findFieldMapIndex("luokka")
    fieldmappings.removeFieldMap(x37)
    x38 = fieldmappings.findFieldMapIndex("pyoravayla")
    fieldmappings.removeFieldMap(x38)
    x39 = fieldmappings.findFieldMapIndex("TEKSTI")
    fieldmappings.removeFieldMap(x39)

    # Spatial join reittien ja liikennevaloristeysten välillä
    arcpy.SpatialJoin_analysis(route, lv_risteys, lv_out, "JOIN_ONE_TO_ONE", "KEEP_ALL", fieldmappings, "INTERSECT", "", "")
    # Poistetaan Join_Count-kenttä jälkikäteen
    arcpy.DeleteField_management(lv_out,"Join_Count")


    # Autoristeysten liittäminen #
    # Luodaan nimi ja polku tiedostolle johon liitetään autoristeykset (count_2)
    auto_join = lv_join.replace("_lv","_auto")
    auto_out = os.path.join(join_fp,auto_join)


    # Fieldmappings
    fieldmappings2 = arcpy.FieldMappings()
    fieldmappings2.addTable(lv_out)
    fieldmappings2.addTable(autoristeys)
    # Haetaan sailytettava kenttä
    sailytettava2 = fieldmappings2.findFieldMapIndex("Join_Count")
    fieldmap2 = fieldmappings2.getFieldMap(sailytettava2)
    # Get the output field's properties as a field object
    field2 = fieldmap2.outputField  
    # Rename the field and pass the updated field object back into the field map
    field2.name = "Count_auto"
    field2.aliasName = "Count_auto"
    fieldmap2.outputField = field2 
    # Set the merge rule and then replace the old fieldmap in the mappings object with the updated one
    fieldmap2.mergeRule = "count"
    fieldmappings2.replaceFieldMap(sailytettava2, fieldmap2)
    
    # Delete fields that are no longer applicable                     
    x2 = fieldmappings2.findFieldMapIndex("TARGET_FID")
    fieldmappings2.removeFieldMap(x2)
    x3 = fieldmappings2.findFieldMapIndex("Join_Count_1")
    fieldmappings2.removeFieldMap(x3)
    x4 = fieldmappings2.findFieldMapIndex("TARGET_FID_1")
    fieldmappings2.removeFieldMap(x4)
    x5 = fieldmappings2.findFieldMapIndex("KLEROTYP")
    fieldmappings2.removeFieldMap(x5)
    x6 = fieldmappings2.findFieldMapIndex("PANIMI_FIN")
    fieldmappings2.removeFieldMap(x6)
    x7 = fieldmappings2.findFieldMapIndex("TIEE_TILA")
    fieldmappings2.removeFieldMap(x7)
    x8 = fieldmappings2.findFieldMapIndex("VAYLATYYPP")
    fieldmappings2.removeFieldMap(x8)
    x9 = fieldmappings2.findFieldMapIndex("TOIMINNALL")
    fieldmappings2.removeFieldMap(x9)
    x10 = fieldmappings2.findFieldMapIndex("TYYPPI")
    fieldmappings2.removeFieldMap(x10)
    x11 = fieldmappings2.findFieldMapIndex("LIIKENNEVI")
    fieldmappings2.removeFieldMap(x11)
    x12 = fieldmappings2.findFieldMapIndex("INV_PAALU_")
    fieldmappings2.removeFieldMap(x12)
    x13 = fieldmappings2.findFieldMapIndex("INV_PAAL_1")
    fieldmappings2.removeFieldMap(x13)
    x14 = fieldmappings2.findFieldMapIndex("VIITE_OID")
    fieldmappings2.removeFieldMap(x14)
    x15 = fieldmappings2.findFieldMapIndex("PAALLYSTE")
    fieldmappings2.removeFieldMap(x15)
    x16 = fieldmappings2.findFieldMapIndex("SILTATAITU")
    fieldmappings2.removeFieldMap(x16)
    x17 = fieldmappings2.findFieldMapIndex("DOCNAME")
    fieldmappings2.removeFieldMap(x17)
    x18 = fieldmappings2.findFieldMapIndex("Laji")
    fieldmappings2.removeFieldMap(x18)
    x19 = fieldmappings2.findFieldMapIndex("Lajin_seli")
    fieldmappings2.removeFieldMap(x19)
    x20 = fieldmappings2.findFieldMapIndex("Z1")
    fieldmappings2.removeFieldMap(x20)
    x21 = fieldmappings2.findFieldMapIndex("Z2")
    fieldmappings2.removeFieldMap(x21)
    x22 = fieldmappings2.findFieldMapIndex("rpastpartc")
    fieldmappings2.removeFieldMap(x22)
    x23 = fieldmappings2.findFieldMapIndex("rpastusety")
    fieldmappings2.removeFieldMap(x23)
    x24 = fieldmappings2.findFieldMapIndex("rpaststatu")
    fieldmappings2.removeFieldMap(x24)
    x25 = fieldmappings2.findFieldMapIndex("RPASTPAVIN")
    fieldmappings2.removeFieldMap(x25)
    x26 = fieldmappings2.findFieldMapIndex("V_LEVEL")
    fieldmappings2.removeFieldMap(x26)
    x27 = fieldmappings2.findFieldMapIndex("RPAPKPARTC")
    fieldmappings2.removeFieldMap(x27)
    x28 = fieldmappings2.findFieldMapIndex("RPAPKUSETY")
    fieldmappings2.removeFieldMap(x28)
    x29 = fieldmappings2.findFieldMapIndex("RPAPKPAVIN")
    fieldmappings2.removeFieldMap(x29)
    x30 = fieldmappings2.findFieldMapIndex("Pituus")
    fieldmappings2.removeFieldMap(x30)
    x31 = fieldmappings2.findFieldMapIndex("NEAR_FID")
    fieldmappings2.removeFieldMap(x31)
    x32 = fieldmappings2.findFieldMapIndex("NEAR_DIST")
    fieldmappings2.removeFieldMap(x32)
    x33 = fieldmappings2.findFieldMapIndex("FID_")
    fieldmappings2.removeFieldMap(x33)
    x34 = fieldmappings2.findFieldMapIndex("TIEE_KUNTA")
    fieldmappings2.removeFieldMap(x34)
    x35 = fieldmappings2.findFieldMapIndex("H_LEVEL")
    fieldmappings2.removeFieldMap(x35)
    x36 = fieldmappings2.findFieldMapIndex("luok_oma")
    fieldmappings2.removeFieldMap(x36)
    x37 = fieldmappings2.findFieldMapIndex("luokka")
    fieldmappings2.removeFieldMap(x37)
    x38 = fieldmappings2.findFieldMapIndex("pyoravayla")
    fieldmappings2.removeFieldMap(x38)
    x39 = fieldmappings2.findFieldMapIndex("TEKSTI")
    fieldmappings2.removeFieldMap(x39)
    
    # Spatial join reittien (joissa lv-risteystieto) ja autoristeysten välillä
    arcpy.SpatialJoin_analysis(lv_out, autoristeys, auto_out, "JOIN_ONE_TO_ONE", "KEEP_ALL", fieldmappings2, "INTERSECT", "", "")
    # Poistetaan Join_Count-kenttä jälkikäteen
    arcpy.DeleteField_management(auto_out,"Join_Count")


    # Kevyen liikenteen risteysten liittäminen #
    # Luodaan nimi ja polku tiedostolle johon liitetään kevyenliikenteen risteykset (count_3)
    kaikki_join = auto_join.replace("_auto","_rist")
    kaikki_out = os.path.join(join_fp,kaikki_join)

    # Fieldmappings
    fieldmappings3 = arcpy.FieldMappings()
    fieldmappings3.addTable(auto_out)
    fieldmappings3.addTable(kevytristeys)
    # Haetaan sailytettava kenttä, esim. objectid
    sailytettava3 = fieldmappings3.findFieldMapIndex("Join_Count")
    fieldmap3 = fieldmappings3.getFieldMap(sailytettava3) 
    # Get the output field's properties as a field object
    field3 = fieldmap3.outputField
    # Rename the field and pass the updated field object back into the field map
    field3.name = "Count_kevyt"
    field3.aliasName = "Count_kevyt"
    fieldmap3.outputField = field3 
    # Set the merge rule and then replace the old fieldmap in the mappings object with the updated one
    fieldmap3.mergeRule = "count"
    fieldmappings3.replaceFieldMap(sailytettava3, fieldmap3)
    
    # Delete fields that are no longer applicable                 
    x2 = fieldmappings3.findFieldMapIndex("TARGET_FID")
    fieldmappings3.removeFieldMap(x2)
    x3 = fieldmappings3.findFieldMapIndex("Join_Count_1")
    fieldmappings3.removeFieldMap(x3)
    x4 = fieldmappings3.findFieldMapIndex("TARGET_FID_1")
    fieldmappings3.removeFieldMap(x4)
    x5 = fieldmappings3.findFieldMapIndex("KLEROTYP")
    fieldmappings3.removeFieldMap(x5)
    x6 = fieldmappings3.findFieldMapIndex("PANIMI_FIN")
    fieldmappings3.removeFieldMap(x6)
    x7 = fieldmappings3.findFieldMapIndex("TIEE_TILA")
    fieldmappings3.removeFieldMap(x7)
    x8 = fieldmappings3.findFieldMapIndex("VAYLATYYPP")
    fieldmappings3.removeFieldMap(x8)
    x9 = fieldmappings3.findFieldMapIndex("TOIMINNALL")
    fieldmappings3.removeFieldMap(x9)
    x10 = fieldmappings3.findFieldMapIndex("TYYPPI")
    fieldmappings3.removeFieldMap(x10)
    x11 = fieldmappings3.findFieldMapIndex("LIIKENNEVI")
    fieldmappings3.removeFieldMap(x11)
    x12 = fieldmappings3.findFieldMapIndex("INV_PAALU_")
    fieldmappings3.removeFieldMap(x12)
    x13 = fieldmappings3.findFieldMapIndex("INV_PAAL_1")
    fieldmappings3.removeFieldMap(x13)
    x14 = fieldmappings3.findFieldMapIndex("VIITE_OID")
    fieldmappings3.removeFieldMap(x14)
    x15 = fieldmappings3.findFieldMapIndex("PAALLYSTE")
    fieldmappings3.removeFieldMap(x15)
    x16 = fieldmappings3.findFieldMapIndex("SILTATAITU")
    fieldmappings3.removeFieldMap(x16)
    x17 = fieldmappings3.findFieldMapIndex("DOCNAME")
    fieldmappings3.removeFieldMap(x17)
    x18 = fieldmappings3.findFieldMapIndex("Laji")
    fieldmappings3.removeFieldMap(x18)
    x19 = fieldmappings3.findFieldMapIndex("Lajin_seli")
    fieldmappings3.removeFieldMap(x19)
    x20 = fieldmappings3.findFieldMapIndex("Z1")
    fieldmappings3.removeFieldMap(x20)
    x21 = fieldmappings3.findFieldMapIndex("Z2")
    fieldmappings3.removeFieldMap(x21)
    x22 = fieldmappings3.findFieldMapIndex("rpastpartc")
    fieldmappings3.removeFieldMap(x22)
    x23 = fieldmappings3.findFieldMapIndex("rpastusety")
    fieldmappings3.removeFieldMap(x23)
    x24 = fieldmappings3.findFieldMapIndex("rpaststatu")
    fieldmappings3.removeFieldMap(x24)
    x25 = fieldmappings3.findFieldMapIndex("RPASTPAVIN")
    fieldmappings3.removeFieldMap(x25)
    x26 = fieldmappings3.findFieldMapIndex("V_LEVEL")
    fieldmappings3.removeFieldMap(x26)
    x27 = fieldmappings3.findFieldMapIndex("RPAPKPARTC")
    fieldmappings3.removeFieldMap(x27)
    x28 = fieldmappings3.findFieldMapIndex("RPAPKUSETY")
    fieldmappings3.removeFieldMap(x28)
    x29 = fieldmappings3.findFieldMapIndex("RPAPKPAVIN")
    fieldmappings3.removeFieldMap(x29)
    x30 = fieldmappings3.findFieldMapIndex("Pituus")
    fieldmappings3.removeFieldMap(x30)
    x31 = fieldmappings3.findFieldMapIndex("NEAR_FID")
    fieldmappings3.removeFieldMap(x31)
    x32 = fieldmappings3.findFieldMapIndex("NEAR_DIST")
    fieldmappings3.removeFieldMap(x32)
    x33 = fieldmappings3.findFieldMapIndex("FID_")
    fieldmappings3.removeFieldMap(x33)
    x34 = fieldmappings3.findFieldMapIndex("TIEE_KUNTA")
    fieldmappings3.removeFieldMap(x34)
    x35 = fieldmappings3.findFieldMapIndex("H_LEVEL")
    fieldmappings3.removeFieldMap(x35)
    x36 = fieldmappings3.findFieldMapIndex("luok_oma")
    fieldmappings3.removeFieldMap(x36)
    x37 = fieldmappings3.findFieldMapIndex("luokka")
    fieldmappings3.removeFieldMap(x37)
    x38 = fieldmappings3.findFieldMapIndex("pyoravayla")
    fieldmappings3.removeFieldMap(x38)
    x39 = fieldmappings3.findFieldMapIndex("TEKSTI")
    fieldmappings3.removeFieldMap(x39)
    
    # Spatial join reittien (joissa liikennevalo- ja autoristeysten määrä) ja kevyen liikenteen risteysten välillä
    arcpy.SpatialJoin_analysis(auto_out, kevytristeys, kaikki_out, "JOIN_ONE_TO_ONE", "KEEP_ALL", fieldmappings3, "INTERSECT", "", "")

   
    # Poistetaan tarpeettomat kentät                                                
    arcpy.DeleteField_management(kaikki_out, "Join_Count")                              
    # Lisätään kenttä risteysten yhteismäärälle
    arcpy.AddField_management(kaikki_out, "Rist_yht", "LONG")
    # lasketaan yhteismäärä                                                            
    expression = "!Count_lv! + !Count_auto! + !Count_kevyt!"
    arcpy.CalculateField_management (kaikki_out, "Rist_yht", expression, "PYTHON")

    # Poistetaan tarpeettomat tiedostot
    arcpy.Delete_management(lv_out)
    arcpy.Delete_management(auto_out)






