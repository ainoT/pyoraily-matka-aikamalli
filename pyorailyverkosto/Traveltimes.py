# -*- coding: cp1252 -*-
# Matka-aikojen laskenta kohteisiin (OD Cost matrix)

import arcpy
import os
from arcpy import env
env.overwriteOutput = True

#Check out the Network Analyst extension license
arcpy.CheckOutExtension("Network")

output_dir = r"{dir_fp}"

# Määritetään parametrit
input_gdb = "{gdb_fp}"
network = os.path.join(input_gdb, "Pyoraily_E", "Pyoraily_E_ND")
layer_name = "OD_Forumiin"
impedance = "Aika4"
accumulate_attributes = ["Aika4","Length"]
restrictions = ["EiPyoralla","Pyoratie","Suomenlinna","Yksisuuntaiset"]
origins = r"{fp}"
destinations = r"{fp}"
output_layer_file = os.path.join(output_dir, layer_name + ".lyrx")
outname = "OD_Forumiin_aika4"

#Create a new OD Cost matrix layer
result_object = arcpy.na.MakeODCostMatrixLayer(network, layer_name, impedance, "", "", accumulate_attributes, "ALLOW_DEAD_ENDS_ONLY", restrictions, "", "", "STRAIGHT_LINES")


#Get the layer object from the result object. The OD cost matrix layer can now be referenced using the layer object.
layer_object = result_object.getOutput(0)

#Get the names of all the sublayers within the OD cost matrix layer.
sublayer_names = arcpy.na.GetNAClassNames(layer_object)
#Stores the layer names that we will use later
origins_layer_name = sublayer_names["Origins"]
destinations_layer_name = sublayer_names["Destinations"]


# Fieldmappings for name
field_mappings1 = arcpy.na.NAClassFieldMappings(layer_object, origins_layer_name)
field_mappings1["Name"].mappedFieldName = "YKR_ID"
#Load the origin locations
arcpy.na.AddLocations(layer_object, origins_layer_name, origins, field_mappings1, "500 Meters", "", "", "", "CLEAR", "NO_SNAP", "", "INCLUDE")

#Load destination
field_mappings2 = arcpy.na.NAClassFieldMappings(layer_object, destinations_layer_name)
field_mappings2["Name"].mappedFieldName = "YKR_ID"
arcpy.na.AddLocations(layer_object, destinations_layer_name, destinations, field_mappings2, "100 Meters", "", "", "", "APPEND", "NO_SNAP", "", "INCLUDE")

#Solve the OD cost matrix layer
arcpy.na.Solve(layer_object)

#Save the solved OD cost matrix layer as a layer file on disk
layer_object.saveACopy(output_layer_file)

# Get a path to the lines sub layer
LinesSubLayer = arcpy.mapping.ListLayers(layer_object, sublayer_names["ODLines"])[0]
line_output = arcpy.CopyFeatures_management(LinesSubLayer, os.path.join(output_dir,"Ruututarkastelu.gdb",outname))

# Lisätään kenttä johon lasketaan lähtöruudun ID (OrigYKR)
arcpy.AddField_management(line_output, "OrigYKR", "LONG")
expression = "int( !Name![0:7] )"
arcpy.CalculateField_management(line_output, "OrigYKR", expression,"PYTHON_9.3")




