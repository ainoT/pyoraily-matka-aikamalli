# -*- coding: cp1252 -*-
# Tieverkon ominaisuustieto reitteihin

import arcpy
import os

# Määritetään workspace      
wspace = r"[dir_fp]"
reitti_ws = os.path.join(wspace,"Reitit.gdb")
arcpy.env.workspace = reitti_ws
arcpy.env.overwriteOutput = True # Sallitaan ylikirjoitus
# Listataan risteystiedot sisältävät reitit
routeList = arcpy.ListFeatureClasses("","","Risteysjoin")

# polku tieverkkoon
tieverkko= r"fp"
        
# Luodaan feature dataset reittien ja tieverkon ominaisuustietojen yhdistelmälle
tieverkkojoinDS = "Tieverkkojoin" 
sp_ref = "[fp]"

if not arcpy.Exists(tieverkkojoinDS):
    arcpy.CreateFeatureDataset_management(reitti_ws, tieverkkojoinDS, sp_ref)

join_fp = os.path.join(reitti_ws, tieverkkojoinDS) # Polku tulosten Feature Datasettiin


# Iteroidaan reittilistaa
for route in routeList:                         
    
    # Luodaan nimi ja polku reittitiedostolle johon liitetään tieverkon ominaisuudet
    road_join = route.replace("_rist","_vayla")
    join_out = os.path.join(join_fp,road_join)
    
    # Fieldmappings siirrettävien tietojen valitsemiseksi
    fieldmappings = arcpy.FieldMappings()
    fieldmappings.addTable(route)
    fieldmappings.addTable(tieverkko)
     
    # Poistetaan tarpeettomia kenttiä                        # olisi voinut tehdä kauniimmin laittamalla kentät listaan!
    x2 = fieldmappings.findFieldMapIndex("TARGET_FID")
    fieldmappings.removeFieldMap(x2)
    x3 = fieldmappings.findFieldMapIndex("Join_Count")
    fieldmappings.removeFieldMap(x3)
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
    x33 = fieldmappings.findFieldMapIndex("FID_")
    fieldmappings.removeFieldMap(x33)


    # Spatial join reittien ja tieverkoston välillä -> HUOM! ei intersect vaan share a line segment
    arcpy.SpatialJoin_analysis(route, tieverkko, join_out, "JOIN_ONE_TO_ONE", "KEEP_ALL", fieldmappings, "SHARE_A_LINE_SEGMENT_WITH", "", "")
    

