# -*- coding: cp1252 -*-

### GPS-PISTEIDEN REITITTÄMINEN PYÖRÄILYVERKOLLE ###

import arcpy
from arcpy import env
import os

#Check out the Network Analyst extension license
arcpy.CheckOutExtension("Network")

### Haetaan reittipistetiedostot ja listataan ne ###
# päähakemisto
ws_dir = r"[dir_fp]"
env.workspace = os.path.join(ws_dir,"GPS_pisteet.gdb")
env.overwriteOutput = True

##fcList = arcpy.ListFeatureClasses("","","Analyysipisteet") # listataan tiedostot
fcList = arcpy.ListFeatureClasses("","","Lenkkireitit") # listataan pätkityt lenkkireittien pisteet
trackList = [] # tehdään samoille datoille workspacesta riippumaton lista


for track in fcList:  
    arcpy.AddField_management(track, "BearingTol", "SHORT")   # Lisätään Bearing Tolerance -kenttä pisteille    
    expression = 30 # toleranssiksi 30 astetta
    arcpy.CalculateField_management(track, "BearingTol", expression)
   
    outfp_dir = os.path.join(ws_dir,"GPS_pisteet.gdb","Lenkkireitit")
    trackList.append(os.path.join(outfp_dir,track))             # Lisätään pistetiedostojen polut uuteen listaan

#------------------------------------------------------------------------------------------------------------------------------------    

# Käydään läpi kaikki listalla olevat gps-pistetiedostot

for gps_track in trackList:

    ### Trackeista erotetaan ensimmäinen ja viimeinen piste route layer stopeiksi ###
    # http://gis.stackexchange.com/questions/143807/how-to-get-values-of-last-row-in-table-with-arcpy-searchcursor

    a_table = gps_track             # läpikäytävä tiedosto
    order_fld = "Id"                # kenttä jonka mukaan järjestetään tiedot laskevasti
    return_flds = ["Id","SHAPE@"]   # palautettavat kentät

    sql_clause = (None,'ORDER BY {} DESC'.format(order_fld)) # järjestetään Id:n perusteella laskevasti, niin viimeinen piste on ensimmäinen

    first_row = ''
    last_row = ''
    with arcpy.da.SearchCursor(a_table, return_flds) as cursor: # normaali järjestys
      first_row = cursor.next()

    with arcpy.da.SearchCursor(a_table, return_flds, sql_clause=sql_clause) as cursor: # laskeva järjestys
      last_row = cursor.next()  # last_row = tuple (Id, PointGeometry)


    first_point = first_row[1]  # haetaan ensimmäiseltä riviltä PointGeometry-objekti
    last_point = last_row[1]    # haetaan viimeiseltä riviltä PointGeometry-objekti
    first_ID = first_row[0]     # tallennetaan ensimmäisen pisteen ID
    last_ID = last_row[0]       # tallennetaan viimeisen pisteen ID


    ### Luodaan GPS-pisteiden avulla restriction-bufferi ###
    # Geometry-oBjekteista http://pro.arcgis.com/en/pro-app/arcpy/classes/geometry.htm

    # Haetaan ja listataan GPS-pisteet Point-objekteina

    array = arcpy.Array()   # luodaan tyhjä array gps-pisteiden listaamista varten
    koord = ''              # tyhjä muuttuja koordinaateille
    # Another cursor
    with arcpy.da.SearchCursor(a_table,["Id","SHAPE@XY"]) as cursor2:
            for row in cursor2:
                koord = row[1]                      # haetaan pisteen koordinaatit
                koordX = koord[0]                   # x-koordinaatti
                koordY = koord[1]                   # y-koordinaatti
                point = arcpy.Point(koordX,koordY)  # tehdään koordinaateista piste
                array.add(point)                    # lisätään piste arrayhin
                if row[0] != last_ID:               # jos ei olla vielä viimeisessä pisteessä, (ks. ylempää)
                    cursor2.next()                  # siirrytään seuraavalle riville

    # pisteistä polyline arrayn avulla
    spatial_ref = arcpy.Describe(gps_track).spatialReference # tallennetaan gps-pistetiedoston koordinaatisto spatial_ref-muuttujaan
    gps_line = arcpy.Polyline(array, spatial_ref, "TRUE", "TRUE") # Polyline(inputs, {spatial_reference}, {has_z}, {has_m})

    # polylinelle bufferi [buffer(distance)]
    gps_buffer = gps_line.buffer(30)                # 30 m scaled cost


    #-----------------------------------------------------------------------------------------------------------------------------------------------------

    ### Make Route Layer ###
    # Tehdään reititystaso

    #Set environment settings
    output_dir = r"[dir_fp]"
    env.workspace = os.path.join(output_dir, "Reitit.gdb")
    env.overwriteOutput = True

    #Set local variables
    input_gdb = r"[gdb_fp]"
    network = os.path.join(input_gdb, "Pyoraily_E", "Pyoraily_E_ND")
    impedance_attribute = "Length"
    buffer_barrier = gps_buffer # bufferi polygon barrieriksi (scaled cost)
    layer_name = "reitti_" + os.path.basename(gps_track)
    
    output_layer_file = os.path.join(output_dir,"Reitit",layer_name + ".lyrx") # reitti-lyrien kopio Reitit-nimiseen kansioon


    # Create a new Route layer
    result_object = arcpy.na.MakeRouteLayer(network, layer_name, impedance_attribute, "USE_INPUT_ORDER", "", "NO_TIMEWINDOWS", "Length", "ALLOW_DEAD_ENDS_ONLY", ["EiPyoralla","Yksisuuntaiset"], "#", "", "TRUE_LINES_WITH_MEASURES")
    #(in_network_dataset, out_network_analysis_layer, impedance_attribute, {find_best_order}, {ordering_type}, {time_windows}, {accumulate_attribute_name}, {UTurn_policy}, {restriction_attribute_name}, {hierarchy}, {hierarchy_settings}, {output_path_shape}, {start_date_time})


    #Get the layer object from the result object. The route layer can now be referenced using the layer object.
    layer_object = result_object.getOutput(0)

    #Get the names of all the sublayers within the route layer.
    sublayer_names = arcpy.na.GetNAClassNames(layer_object)
    #Stores the layer names that we will use later
    stops_layer_name = sublayer_names["Stops"]
    restriction_layer_name = sublayer_names["PolylineBarriers"]
    polygon_layer_name = sublayer_names["PolygonBarriers"]
    reittinimi = str(os.path.basename(gps_track))

    ## FieldMappings
    # FieldMappings bufferi-polygonin attribuuttien muuttamiseksi
    fieldMappings = arcpy.na.NAClassFieldMappings(layer_object, polygon_layer_name)

    # Haetaan FieldMapit tyyppi- ja pituus-muuttujille
    fieldMap1 = fieldMappings["BarrierType"]
    fieldMap2 = fieldMappings["Attr_Length"]

    # Barrier type on scaled cost
    fieldMap1.defaultValue = 1 # Scaled Cost
    
    #Polygonin sisällä matkat ovat 0.1 kertaa "lyhyempiä" (=edullisempia)
    fieldMap2.defaultValue = 0.1
    

    ### Add locations ###
    # Alku ja loppu GPS-pisteiden ja rajoitusbufferin lisääminen ND-verkostoon

    # Lisätään scaled cost bufferi (30 m)
    arcpy.na.AddLocations(layer_object, polygon_layer_name, buffer_barrier, fieldMappings, "", "",[["pyorailyverkko_E_tm35fin","SHAPE"],["Pyoraily_E_ND_Junctions","NONE"]], "MATCH_TO_CLOSEST", "CLEAR")

    # Lisätään alkupiste
    # Snap verkostoon, exclude kielletyille alueille sijoittamisessa, hyödyntää Bearing kenttiä, etsintäsäde 30 m (pysyy bufferin sisällä)
    arcpy.na.AddLocations(layer_object, stops_layer_name, first_point, "", "30 Meters", "",[["pyorailyverkko_E_tm35fin","SHAPE"],["Pyoraily_E_ND_Junctions","NONE"]], "MATCH_TO_CLOSEST", "APPEND", "SNAP", "0 Meters", "EXCLUDE")
    #(in_network_analysis_layer, sub_layer, in_table, field_mappings, search_tolerance, {sort_field}, {search_criteria}, {match_type}, {append}, {snap_to_position_along_network}, {snap_offset}, {exclude_restricted_elements}, {search_query})

    # Lisätään loppupiste, huom APPEND
    arcpy.na.AddLocations(layer_object, stops_layer_name, last_point, "", "30 Meters", "",[["pyorailyverkko_E_tm35fin","SHAPE"],["Pyoraily_E_ND_Junctions","NONE"]], "MATCH_TO_CLOSEST", "APPEND", "SNAP", "0 Meters", "EXCLUDE")



    ### Solve the route layer ###
    arcpy.na.Solve(layer_object, "SKIP", "CONTINUE") # ohitetaan löytymättömät stopit; jatketaan solvea vaikka jollain reitillä tulisi virhe


    # Save the solved route layer as a layer file on disk
    layer_object.saveACopy(output_layer_file) # kopio reitistä erilliseen kansioon


    # Kopioidaan pelkkä reitti (jos sellainen on muodostunut)
    
    outRoutesSubLayer = arcpy.mapping.ListLayers(layer_object, sublayer_names["Routes"])[0] # Get a path to the routes sub layer
    
    route_cnt = int(arcpy.GetCount_management(outRoutesSubLayer).getOutput(0))   # haetaan reittien lukumäärä
    if route_cnt < 1:
        print("Ei ratkaisua trackille " + reittinimi)  # jos reittiä ei ole muodostunut (lkm < 1), printataan sen nimi
    else:
        print("Reitti ratkaistu trackille " + reittinimi)       # jos reitti on muodostunut, printataan nimi ja tallennetaan Reitit.gdb:hen

        # Save the resulting route polyline (the Routes Sublayer) to disk
        route_output = arcpy.CopyFeatures_management(outRoutesSubLayer, layer_name)

        name_expression = "'" + reittinimi + "'"                                                    # lisätään hipsut jotta päivittyy oikein
        arcpy.CalculateField_management(route_output, "Name", name_expression,"PYTHON_9.3")         # lisätään tiedoston nimi Name-kenttään 
        arcpy.CalculateField_management(route_output, "Total_Length", "!SHAPE.LENGTH!","PYTHON_9.3")# Total_Length -kentässä nyt x10 pienempi arvo, lasketaan todellinen pituus


        
    ### POISTA LOPUKSI TURHAT OBJEKTIT ### 
    arcpy.Delete_management(gps_line)
    arcpy.Delete_management(gps_buffer)



