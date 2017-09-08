# -*- coding: cp1252 -*-
# Analysoitavat GPS-tiedostot csv:ksi #
# http://gis.stackexchange.com/questions/109008/python-script-to-export-csv-tables-from-gdb


import arcpy
import os
import csv

# Määritetään päähakemisto      
ws_dir = r"[dir_fp]"
# GPS-pisteiden hakemisto
GPS_fp = os.path.join(ws_dir,"GPS_pisteet.gdb")

# Haetaan reittipistetiedostot ja listataan ne
arcpy.env.workspace = GPS_fp
# Listataan GPS-pisteet omista dataseteistaan
analyysiList = arcpy.ListFeatureClasses("","","Analyysipisteet") # analyysipisteet
korvaavatList = arcpy.ListFeatureClasses("","","Korvaavat") # korvaavat pisteet
lenkkiList = arcpy.ListFeatureClasses("","","Lenkkireitit") # analysoitujen lenkkireittien pisteet

# Yhdistetään kaikki listat
kaikki_pisteet = analyysiList + korvaavatList + lenkkiList

# Lisätään kaikkien pisteiden tiedot yhteen csv-tauluun
out_fp = r"[dir_fp]"
outfile = os.path.join(out_fp,"GPS_reitit_join.csv")

# Luupataan kaikki pisteet 
for table in kaikki_pisteet:
    
    fields = arcpy.ListFields(table)                # listataan kentät
    field_names = [field.name for field in fields]  # tehdään kenttien nimistä lista
    iter_round = kaikki_pisteet.index(table)        # määritetään luupin iterointikierros
    with open(outfile,'ab') as f:                   # avataan csv-tiedosto 'append'-muodossa
            w = csv.writer(f)
            if iter_round == 0:                     # jos kyseessä ensimmäinen iterointikierros
                w.writerow(field_names)             # kirjoitetaan kenttien nimet
                for row in arcpy.SearchCursor(table):
                    field_vals = [row.getValue(field.name) for field in fields]
                    w.writerow(field_vals)
                del row
            else:                                   # muilla kierroksilla kenttien nimiä ei kirjoiteta
                for row in arcpy.SearchCursor(table):
                    field_vals = [row.getValue(field.name) for field in fields]
                    w.writerow(field_vals)
                del row



