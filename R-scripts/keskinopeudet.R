# GPS-aineiston keskinopeudet

rm(list=ls()) #Clear all data

setwd("filepath")

taulukko = ("GPS_pisteet.csv")
gps = read.csv(taulukko, header = TRUE)
attach(gps)
summary(gps)


# boxplot nopeuksista py�r�ilij�n mukaan jaoteltuna
boxplot(SPEED_mps ~ CycID, horizontal=FALSE, xlab="Py�r�ilij� ID", ylab="Nopeus (m/s)")

# Lis�t��n sarakkeet py�r�ilij�n ja reittien keskinopeuksille
gps[,"C_avgspeed"]  <- ""
gps[,"R_avgspeed"]  <- ""
gps[,"C_medianspeed"]  <- ""
gps[,"R_medianspeed"]  <- ""

attach(gps)


# Tietojen haku uuteen dataframeen
df <- data.frame(CycID, DISTANCE_m, DURATION_s, SPEED_mps, Trackname, R_part, from_start, R_avgspeed, C_avgspeed, C_medianspeed, R_medianspeed, stringsAsFactors=F)

# Lasketaan ryhmitt�in
# nopeuden keskiarvo / py�r�ilij�
C_ka_S = aggregate(SPEED_mps ~ CycID, df, mean)
# nopeuden mediaani / py�r�ilij�
C_md_S = aggregate(SPEED_mps ~ CycID, df, median)
# nopeuden keskiarvo / reitti
R_ka_S = aggregate(SPEED_mps ~ Trackname, df, mean)      
# nopeuden mediaani / reitti
R_md_S = aggregate(SPEED_mps ~ Trackname, df, median)


# Lasketaan lis�� tunnuslukuja
# py�r�ilij�n nopeuden keskihajonta
C_sd_S = aggregate(SPEED_mps ~ CycID, gps, sd)
# py�r�ilij�n miniminopeus
C_min_S = aggregate(SPEED_mps ~ CycID, gps, min)
# py�r�ilij�n maksiminopeus
C_max_S = aggregate(SPEED_mps ~ CycID, gps, max)

# yhdistet��n tiedot samaan dataframeen
C_ka_S[,"C_avgspeed"]  <- C_ka_S[,"SPEED_mps"]
C_ka_S[,"C_medianspeed"]  <- C_md_S[,"SPEED_mps"]
C_ka_S[,"C_stdspeed"]  <- C_sd_S[,"SPEED_mps"]
C_ka_S[,"C_minspeed"] <- C_min_S[,"SPEED_mps"]
C_ka_S[,"C_maxspeed"] <- C_max_S[,"SPEED_mps"]

# Yhteenveto tiedoista
summary(C_ka_S)

# kirjoitetaan csv:ksi
write.csv(C_ka_S, "Pyorailijat_nopeus_uusi.csv", row.names=FALSE)



# Reitit
# Lis�t��n reittien dataframeen kentti�
R_ka_S[,"R_avgspeed"]  <- R_ka_S$SPEED_mps
R_ka_S[,"R_medianspeed"] <- ""
R_ka_S[,"R_minspeed"]  <- ""
R_ka_S[,"R_maxspeed"]  <- ""
R_ka_S[,"R_stdspeed"]  <- ""

# Reitin miniminopeus
R_min_S = aggregate(SPEED_mps ~ Trackname, gps, min)
# Reitin maksiminopeus
R_max_S = aggregate(SPEED_mps ~ Trackname, gps, max)
# Reitin nopeuden keskihajonta
R_sd_S = aggregate(SPEED_mps ~ Trackname, gps, sd)

# Lis�t��n lasketut dataframeen
R_ka_S <- within(R_ka_S, R_medianspeed <- R_md_S$SPEED_mps)
R_ka_S <- within(R_ka_S, R_minspeed <- R_min_S$SPEED_mps)
R_ka_S <- within(R_ka_S, R_maxspeed <- R_max_S$SPEED_mps)
R_ka_S <- within(R_ka_S, R_stdspeed <- R_sd_S$SPEED_mps)

# Yhteenveto
summary(R_ka_S)

# kirjoitetaan csv:ksi
write.csv(R_ka_S, "Alkup_reitit_nopeus.csv", row.names=FALSE)


#-----------------------------------------------------------------------
rm(list=ls())
# Tarkastellaan py�r�ilij�kohtaisia nopeuksia lis��
setwd("fp")

table = ("Pyorailijat_nopeus_uusi.csv")
pyorailijat = read.csv(table, header = TRUE)
attach(pyorailijat)
summary(pyorailijat)

table2 = ("Datat_yhdessa_2017.csv")
taustadata = read.csv(table2, header = TRUE, sep = ";")
summary(taustadata)
attach(taustadata)

# taustadatallekin CycID
taustadata[,"CycID"] <- TallID


# Yhdistet��n tiedot
noptausta = merge(taustadata, pyorailijat, by = "CycID")

# kirjoitetaan csv:ksi
write.csv(noptausta, "Pyorailijat_ja_nopeudet.csv", row.names=FALSE)

########################################################################
rm(list=ls())
setwd("fp")

table3 = ("Pyorailijat_ja_nopeudet.csv")
noptausta = read.csv(table3, header = TRUE, sep = ",")
attach(noptausta)
summary(noptausta)

hist(Ika, main="Vastaajien ik�jakauma", breaks=10, xlab="Ik�", ylab="Vastaajia", col="light grey")

boxplot(C_avgspeed, xlab="kaikki", ylab="Keskinopeus (m/s)")

# dummy-muuttuja "kaikki" visualisointeja varten
noptausta[,"Kaikki"] <- "kaikki"

# Keskinopeus sukupuolittain
boxplot(C_avgspeed ~ Sukupuoli_text, xlab="Sukupuoli", ylab="Keskinopeus (m/s)")
boxplot(C_avgspeed ~ Sukupuoli_text, plot=FALSE)
# Reittien m��r� ryhmitt�in (reittien n=1345 ilman virheellisten poistoja)
aggregate(Ratkaistu_kaikki ~ Sukupuoli_text, noptausta, sum)

# Samaan kuvaan
par(mfrow=c(1,2))
boxplot(C_avgspeed, xlab="Kaikki", ylab="Keskinopeus (m/s)")
boxplot(C_avgspeed ~ Sukupuoli_text, xlab="Sukupuoli", ylab="Keskinopeus (m/s)")
par(mfrow=c(1,1))


# Tekstimuotoiset arvot py�r�ilyaktiivisuudelle ja talvipy�r�ilylle + ik�ryhm�t
noptausta[,"Aktiivisuus"] <- ""
noptausta[,"Talvi"] <- ""
noptausta[,"Ikaluokka"] <- ""
noptausta[,"Ikaluokka2"] <- ""

attach(noptausta)

# Annetaan aktiivisuuksille arvot
noptausta <- within(noptausta, Aktiivisuus[Pyorailyaktiivisuus == 3] <- '1-2 p�iv�n� viikossa')
noptausta <- within(noptausta, Aktiivisuus[Pyorailyaktiivisuus == 4] <- '3-5 p�iv�n� viikossa')
noptausta <- within(noptausta, Aktiivisuus[Pyorailyaktiivisuus == 5] <- '6-7 p�iv�n� viikossa')
noptausta <- within(noptausta, Talvi[Talvipyoraily == 0] <- 'En lainkaan')
noptausta <- within(noptausta, Talvi[Talvipyoraily == 1] <- 'Satunnaisesti')
noptausta <- within(noptausta, Talvi[Talvipyoraily == 2] <- 'S��nn�llisesti')


# Luokitellaan ik�
noptausta <- within(noptausta, Ikaluokka[Ika < 20] <- '< 20')
noptausta <- within(noptausta, Ikaluokka[Ika >= 20 & Ika < 25] <- '20-25')
noptausta <- within(noptausta, Ikaluokka[Ika >= 25 & Ika < 30] <- '25-30')
noptausta <- within(noptausta, Ikaluokka[Ika >= 30 & Ika < 35] <- '30-35')
noptausta <- within(noptausta, Ikaluokka[Ika >= 35 & Ika < 40] <- '30-40')
noptausta <- within(noptausta, Ikaluokka[Ika >= 40 & Ika < 45] <- '40-45')
noptausta <- within(noptausta, Ikaluokka[Ika >= 45 & Ika < 50] <- '45-50')
noptausta <- within(noptausta, Ikaluokka[Ika >= 50 & Ika < 55] <- '50-55')
noptausta <- within(noptausta, Ikaluokka[Ika >= 55] <- '55-60')


# Keskinopeus i�n mukaan
boxplot(C_avgspeed ~ Ikaluokka, xlab="Ik�",ylab="Keskinopeus (m/s)") 
boxplot(C_avgspeed ~ Ikaluokka, plot=FALSE) # tuottaa summaryn

# Reittien m��r� ik�ryhmitt�in
aggregate(Ratkaistu_kaikki ~ Ikaluokka, noptausta, sum)

# Luokitellaan ik� 10 v v�lein
noptausta <- within(noptausta, Ikaluokka2[Ika < 20] <- '< 20')
noptausta <- within(noptausta, Ikaluokka2[Ika >= 20 & Ika < 30] <- '20-30')
noptausta <- within(noptausta, Ikaluokka2[Ika >= 30 & Ika < 40] <- '30-40')
noptausta <- within(noptausta, Ikaluokka2[Ika >= 40 & Ika < 50] <- '40-50')
noptausta <- within(noptausta, Ikaluokka2[Ika >= 50] <- '50-60')

boxplot(C_avgspeed ~ Ikaluokka2, xlab="Ik�",ylab="Keskinopeus (m/s)")
boxplot(C_avgspeed ~ Ikaluokka2, plot=FALSE) # tuottaa summaryn


# Nopeuden ja i�n korrelaatio
cor.test(C_avgspeed, Ika, method="pearson") # -0.1288473, p-value = 0.4045 -> Ei merkitsev�� korrelaatiota
cor.test(C_avgspeed, Ika, method="spearman") # -0.1977202, p-value = 0.1983 -> Ei merkitsev�� korrelaatiota


# Keskinopeus ja py�r�ilyaktiivisuus

# Tietojen p�ivitt�minen dataframeen toisesta sarakkeesta
df <- data.frame(CycID,Pyorailyaktiivisuus, Aktiivisuus, Talvipyoraily, Talvi, C_avgspeed, C_medianspeed, C_maxspeed, C_minspeed, C_stdspeed, Kuvaile, Reittikuvailu, Ika, Ikaluokka, Ratkaistu_kaikki, Tilastovaiheessa, stringsAsFactors=F)
# poistetaan puuttuva tieto ID 40 (rivi 36)
df <- df[-c(36), ]

# Py�r�ilyaktiivisuus
boxplot(df$C_avgspeed ~ df$Aktiivisuus, xlab="Py�r�ilyaktiivisuus", ylab="Keskinopeus (m/s)")
boxplot(df$C_avgspeed ~ df$Aktiivisuus, plot=FALSE)
# Korrelaatio
cor.test(df$C_avgspeed, df$Pyorailyaktiivisuus, method="spearman") # 0.4539739, p-value = 0.00223 -> Merkitsev� korrelaatio!
# Reittien m��r� ryhmitt�in
aggregate(df$Ratkaistu_kaikki ~ df$Aktiivisuus, df, sum)

# Talvipy�r�ily
boxplot(df$C_avgspeed ~ df$Talvi, xlab="Py�r�iletko talvella?", ylab="Keskinopeus (m/s)")
boxplot(df$C_avgspeed ~ df$Talvi, plot=FALSE)
# Korrelaatio
cor.test(df$C_avgspeed, df$Talvipyoraily, method="spearman") # 0.4305046, p-value = 0.003956 -> Merkitsev� korrelaatio!
# Reittien m��r� ryhmitt�in
aggregate(df$Ratkaistu_kaikki ~ df$Talvi, df, sum)



# Py�r�ilyaktiivisuus
# Stratified boxplots
# https://www.youtube.com/watch?v=s7ljwAzB5dQ 
boxplot(Track_lkm ~ Sukupuoli_text*Aktiivisuus, horizontal=TRUE)

