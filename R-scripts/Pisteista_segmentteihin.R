# Aggregoidaan pisteiden tiedot 50 m reittisegmentteihin

rm(list=ls()) #Clear all data

setwd("fp")

taulukko = ("GPS_reitit_join.csv")
gps = read.csv(taulukko, header = TRUE)

# Lis‰t‰‰n kentt‰, johon lasketaan tunniste jokaiselle 50 m reittisegmentille
gps[,"segmentID"]  <- ""

attach(gps)

# Tehd‰‰n NEAR_FIDist‰ tekstimuotoinen muuttuja
nearFIDtxt = as.character(gps$NEAR_FID)
# Tehd‰‰n CycID:st‰ tekstimuotoinen muuttuja
CycIDtxt = as.character(gps$CycID)

# yhdistet‰‰n reitin nimen kanssa ja lis‰t‰‰n tieto kentt‰‰n
gps <- within(gps, segmentID <- paste(CycIDtxt, gps$Name_1, nearFIDtxt))

# Annetaan count-kenttien NA-arvoille arvo 0
gps <- within(gps, Count_lv[is.na(Count_lv)] <- 0)
gps <- within(gps, Count_auto[is.na(Count_auto)] <- 0)
gps <- within(gps, Count_kevyt[is.na(Count_kevyt)] <- 0)

# Lasketaan risteysten yhteism‰‰r‰
# annetaan ensin arvoksi 0 (ovat oletuksena NA)
gps <- within(gps, Rist_yht <- 0)
gps <- within(gps, Rist_yht <- (Count_lv + Count_auto + Count_kevyt))


# Lasketaan ryhmitt‰in
# Tehd‰‰n uusi dataframe, johon aggregoidaan segmenttikohtanen nopeuden keskiarvo, ja aletaan lis‰t‰ tarpeellisia kentti‰
segmentit = aggregate(SPEED_mps ~ segmentID, gps, mean)

# nopeuden mediaani
S_md = aggregate(SPEED_mps ~ segmentID, gps, median)
# miniminopeus
S_min = aggregate(SPEED_mps ~ segmentID, gps, min)
# maksiminopeus
S_max = aggregate(SPEED_mps ~ segmentID, gps, max)
# nopeuden keskihajonta
S_sd = aggregate(SPEED_mps ~ segmentID, gps, sd)
# et‰isyyden summa
Dist_sum = aggregate(DISTANCE_m ~ segmentID, gps, sum)      
# ajan summa
Time_sum = aggregate(DURATION_s ~ segmentID, gps, sum)      

# pisteiden m‰‰r‰/segmentti
# count R:ss‰ http://www.theanalysisfactor.com/r-tutorial-count/
# count-funktio
count <- function(NEAR_FID){ length(NEAR_FID) }

Count_gps = aggregate(NEAR_FID ~ segmentID, gps, count) 

# Aggregoidaan muut tarvittavat tiedot
gradientti = aggregate(Gradientti ~ segmentID, gps, min)
Tot_pituus = aggregate(Total_pituus ~ segmentID, gps, min)
rist_lv = aggregate(Count_lv ~ segmentID, gps, min)
rist_auto = aggregate(Count_auto ~ segmentID, gps, min)
rist_kevyt = aggregate(Count_kevyt ~ segmentID, gps, min)
rist_yht = aggregate(Rist_yht ~ segmentID, gps, min)
kunta = aggregate(TIEE_KUNTA ~ segmentID, gps, min, na.action = na.pass)
H_lev = aggregate(H_LEVEL ~ segmentID, gps, min, na.action = na.pass)           
omaluokka = aggregate(luok_oma ~ segmentID, gps, min, na.action = na.pass)      
Tieluokka = aggregate(luokka ~ segmentID, gps, min, na.action = na.pass)        
Pyoraluokka = aggregate(pyoravayla ~ segmentID, gps, min, na.action = na.pass)  
seg_pituus = aggregate(Shape_Length ~ segmentID, gps, min, na.action = na.pass)


# Lis‰t‰‰n vanhat kent‰t
segmentit[,"Gradientti"]  <- gradientti[,"Gradientti"]
segmentit[,"Reittipituus"]  <- Tot_pituus[,"Total_pituus"]
segmentit[,"Rist_lv"]  <- rist_lv[,"Count_lv"]
segmentit[,"Rist_auto"]  <- rist_auto[,"Count_auto"]
segmentit[,"Rist_kevyt"]  <- rist_kevyt[,"Count_kevyt"]
segmentit[,"Rist_yht"]  <- rist_yht[,"Rist_yht"]
segmentit[,"Kuntanro"]  <- kunta[,"TIEE_KUNTA"]               
segmentit[,"H_LEVEL"]  <- H_lev[,"H_LEVEL"]
segmentit[,"luokka_oma"]  <- omaluokka[,"luok_oma"]
segmentit[,"Tieluokitus"]  <- Tieluokka[,"luokka"]
segmentit[,"Pyoravayla"]  <- Pyoraluokka[,"pyoravayla"]
segmentit[,"Seg_pituus"]  <- seg_pituus[,"Shape_Length"]

# Lis‰t‰‰n uudet kent‰t
segmentit[,"Speed_md"]  <- S_md[,"SPEED_mps"]
segmentit[,"Speed_min"]  <- S_min[,"SPEED_mps"]
segmentit[,"Speed_max"]  <- S_max[,"SPEED_mps"]
segmentit[,"Speed_sd"]  <- S_sd[,"SPEED_mps"]
segmentit[,"matka"]  <- Dist_sum[,"DISTANCE_m"]
segmentit[,"aika"]  <- Time_sum[,"DURATION_s"]
segmentit[,"Count_gps"]  <- Count_gps[,"NEAR_FID"]


# Erotetaan reitin nimi
library(stringr)
nimisplit = str_split_fixed(segmentit$segmentID, " ", 3)  
# lis‰t‰‰n uuteen kentt‰‰ reitin nimi
segmentit[,"Nimi"]  <- nimisplit[,2]


# Reitin keskinopeus ja segmentin nopeuden ero siihen
# merge https://www.stat.berkeley.edu/~spector/Rcourse.pdf s.35 (slaidi 70)

# Aggregoidaan reitin keskinopeus
reitti_nop_ka = aggregate(SPEED_mps ~ Nimi, segmentit, mean) 

# reitin mediaaninopeus
reitti_nop_md = aggregate(SPEED_mps ~ Nimi, segmentit, median)

# Merge
segmentit_merge = merge(segmentit, reitti_nop_ka, by="Nimi")
segmentit_kaikki = merge(segmentit_merge, reitti_nop_md, by="Nimi")

# Lis‰t‰‰n mergettyihin segmentteihin kentt‰, johon lasketaan erotus
# segmentin keskinopeus - reitin keskinopeus 
segmentit_kaikki[,"Nop_ka_ero"] <- (segmentit_kaikki$SPEED_mps.x - segmentit_kaikki$SPEED_mps.y)
# segmentin mediaaninopeus - reitin mediaaninopeus
segmentit_kaikki[,"Nop_md_ero"] <- (segmentit_kaikki$Speed_md - segmentit_kaikki$SPEED_mps)


# Kirjoitetaan tiedostoksi
write.csv(segmentit_kaikki, "Segmentit_kaikki.csv", row.names=FALSE)

# ---------------------------------------------------------------------
# Erota kuukausittaiset nopeudet

rm(list=ls()) #Clear all data

setwd("fp")
table = ("GPS_reitit_join.csv")
gps = read.csv(table, header = TRUE)

# uudet kent‰t vuodelle ja kuukaudelle
gps[,"vuosi"]  <- ""
gps[,"kuukausi"]  <- ""

attach(gps)

# Erotetaan reitin nimi
library(stringr)
aikasplit = str_split_fixed(DateTimeS, "-", 3)  

# lis‰t‰‰n kuukausi ja vuosi kenttiins‰
gps[,"vuosi"]  <- as.integer(aikasplit[,1])
gps[,"kuukausi"]  <- aikasplit[,2]

attach(gps)

# Boxplot kuukausittaisista nopeuksista
boxplot(SPEED_mps ~ kuukausi, xlab="kuukausi", ylab="Keskinopeus (m/s)")
boxplot(SPEED_mps ~ kuukausi, plot=FALSE)
boxplot(SPEED_mps, plot = FALSE)

# Samaan kuvaan         -> ei n‰yt‰ hyv‰lt‰
par(mfrow=c(1,2))
boxplot(SPEED_mps, xlab="kaikki", ylab="Keskinopeus (m/s)")
boxplot(SPEED_mps ~ kuukausi, xlab="kuukausi", ylab="Keskinopeus (m/s)")
par(mfrow=c(1,1))

summary(gps)

vuosisort = gps[order(vuosi),]

