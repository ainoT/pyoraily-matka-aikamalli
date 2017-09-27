# Segmenttien analyysi
rm(list=ls())

setwd("fp")

table = ("Segmentit_kaikki_editoitu.csv")
segmentit = read.csv(table, header = TRUE)

attach(segmentit)
summary(segmentit)


# nimet:
# SPEED_mps.x = segmentin keskinopeus
# Speed_md = segmentin mediaaninopeus
# + min, max, sd 
# SPEED_mps.y = reitin keskinopeus
# SPEED_mps = reitin mediaaninopeus                         # voisi nimetä paremmin uudelleen...
# Nop_ka_ero = segmentin keskinopeus - reitin keskinopeus 
# Nop_md_ero = segmentin mediaaninopeus - reitin mediaaninopeus

# Boxplotteja ja dotplotteja #

# GPS count (uusi)
dotchart(Count_gps, main = "GPS-pisteiden määrä segmentillä",
         xlab = "Range of data", 
         ylab = "Order of the data")
boxplot(Count_gps, main = "GPS-pisteiden määrä segmentillä", horizontal = TRUE)

# sorttaus gps countin mukaan
#sortattu <- segmentit[order(-Count_gps),] 
# sort ajan mukaan
aikasort <- segmentit[order(-aika),] # nopeudet melko normaaleja
# sort matkan mukaan
matkasort <- segmentit[order(-matka),] # nopeudet melko normaaleja

# Tarkista aggregoinnilla reittien määrä
lkm_testi = aggregate(Gradientti ~ Nimi, segmentit, mean) # 1329 

# segmentin keskinopeus
boxplot(SPEED_mps.x, main = "Segmentin keskinopeus (m/s)", horizontal = TRUE) 
dotchart(SPEED_mps.x, main = "Segmentin keskinopeus (m/s)",
         xlab = "Range of data", 
         ylab = "Order of the data")
# sortataan segmentin keskinopeuden mukaan
sort_ka_nop = segmentit[order(-SPEED_mps.x),]


# Reitin keskinopeus
boxplot(SPEED_mps.y, main = "Reitin keskinopeus (m/s)", horizontal = TRUE)
dotchart(SPEED_mps.y, main = "Reitin keskinopeus (m/s)",
         xlab = "Range of data", 
         ylab = "Order of the data")

# Segmentin keskinopeuden ero reitin nopeuden keskiarvosta
boxplot(Nop_ka_ero, main = "Nopeuden ero keskiarvosta (m/s)", horizontal = TRUE) 
dotchart(Nop_ka_ero, main = "Nopeuden ero keskiarvosta (m/s)",
         xlab = "Range of data", 
         ylab = "Order of the data")

# Segmentin mediaaninopeuden ero reitin mediaaninopeudesta
boxplot(Nop_md_ero, main = "Nopeuden ero mediaanista (m/s)", horizontal = TRUE)
dotchart(Nop_md_ero, main = "Nopeuden ero mediaanista (m/s)",
         xlab = "Range of data", 
         ylab = "Order of the data")

# Gradientti
boxplot(Gradientti, main = "Gradientti %", horizontal = TRUE)
dotchart(Gradientti, main = "Gradientti %")
hist(Gradientti)
qqnorm(Gradientti)
qqline(Gradientti, col = "red") # ei normaali 

# Aika
boxplot(aika, main = "Aika (s)", horizontal = TRUE)
dotchart(aika, main = "Aika (s)")
hist(aika) # erittäin epänormaali
qqnorm(aika)
qqline(aika, col = "red")

# Kaikki risteykset
boxplot(Rist_yht, main = "Risteysten lkm", horizontal = TRUE)
dotchart(Rist_yht, main = "Risteysten lkm")
hist(Rist_yht)


# # Tutki normaalisuutta
# # keskiarvo
# hist(SPEED_mps.x)
# ks.test(SPEED_mps.x, y=rnorm) #
# ad.test(SPEED_mps.x) # pieni p-arvo
# # Q-Q plot
# qqnorm(SPEED_mps.x)
# qqline(SPEED_mps.x, col = "red") # oikeata yläkulmaa lukuunottamatta normaalin oloinen
# 
# # mediaani
# hist(Speed_md)
# ks.test(Speed_md, y=rnorm) #
# ad.test(Speed_md) # pieni p-arvo
# # Q-Q plot
# qqnorm(Speed_md)
# qqline(Speed_md, col = "red") #



# Scatterplotteja ja korrelaatioita
# Segmentin keskinopeus ja gradientti
plot(Gradientti,SPEED_mps.x, xlab = "Gradientti (%)", ylab = "Keskinopeus (m/s)")
text(23,19, round(cor(Gradientti,SPEED_mps.x,method = "pearson"),3))
cor.test(Gradientti,SPEED_mps.x,method = "spearman") # -0.2306587, selitysaste 0.05320344, p-value < 2.2e-16
cor.test(Gradientti,SPEED_mps.x,method = "pearson") # -0.2016445, p-value < 2.2e-16 => korrelaatiot merkitseviä

# Segmentin keskinopeus ja kaikki risteykset
plot(Rist_yht,SPEED_mps.x, xlab = "Risteysten lkm", ylab="Keskinopeus (m/s)")
text(6.5,18, round(cor(Rist_yht,SPEED_mps.x,method = "pearson"),3))
cor.test(Rist_yht,SPEED_mps.x,method = "spearman") # -0.1834179, p-value < 2.2e-16
cor.test(Rist_yht,SPEED_mps.x,method = "pearson") # -0.2025249, p-value < 2.2e-16

# Segmentin keskinopeus ja liikennevaloristeykset
plot(Rist_lv,SPEED_mps.x, xlab = "Liikennevalojen lkm", ylab = "Keskinopeus (m/s)")
text(4.5,18, round(cor(Rist_lv,SPEED_mps.x,method = "pearson"),3))
cor.test(Rist_lv,SPEED_mps.x,method = "spearman") # -0.1315686, p-value < 2.2e-16
cor.test(Rist_lv,SPEED_mps.x,method = "pearson") # -0.1361548, p-value < 2.2e-16

# Segmentin keskinopeus ja autoristeykset
plot(Rist_auto,SPEED_mps.x, xlab = "Liikennevalottomien risteysten lkm", ylab = "Keskinopeus (m/s)")
text(4.5,18, round(cor(Rist_auto,SPEED_mps.x,method = "pearson"),3))
cor.test(Rist_auto,SPEED_mps.x,method = "spearman") # -0.06912381, p-value < 2.2e-16
cor.test(Rist_auto,SPEED_mps.x,method = "pearson") # -0.06860376, p-value < 2.2e-16

# Segmentin keskinopeus ja kevyen liikenteen risteykset
plot(Rist_kevyt,SPEED_mps.x, xlab = "Kevyen liik. risteysten lkm", ylab = "Keskinopeus (m/s)")
text(6.5,18, round(cor(Rist_kevyt,SPEED_mps.x,method = "pearson"),3))
cor.test(Rist_kevyt,SPEED_mps.x,method = "spearman") # -0.1492339, p-value < 2.2e-16
cor.test(Rist_kevyt,SPEED_mps.x,method = "pearson") # -0.1585915, p-value < 2.2e-16



## Scatterplotit keskinopeuden muutokseen
# Segmentin keskinopeuden muutos reitin keskinopeudesta ja gradientti
plot(Gradientti,Nop_ka_ero, xlab = "Gradientti (%)", ylab = "Muutos keskinopeudesta (m/s)")
text(23,13, round(cor(Gradientti,Nop_ka_ero,method = "pearson"),3))
cor.test(Gradientti,Nop_ka_ero,method = "spearman") # -0.2916751, p-value < 2.2e-16
cor.test(Gradientti,Nop_ka_ero,method = "pearson") # -0.2431304, p-value < 2.2e-16

# Segmentin keskinopeuden muutos reitin keskinopeudesta ja kaikki risteykset
plot(Rist_yht,Nop_ka_ero, xlab = "Risteysten lkm", ylab = "Muutos keskinopeudesta (m/s)")
text(6.5,11, round(cor(Rist_yht,Nop_ka_ero,method = "pearson"),3))
cor.test(Rist_yht,Nop_ka_ero,method = "spearman") # -0.1779074, p-value < 2.2e-16
cor.test(Rist_yht,Nop_ka_ero,method = "pearson") # -0.2061343, p-value < 2.2e-16

# Segmentin keskinopeuden muutos reitin keskinopeudesta ja lv-risteykset
plot(Rist_lv,Nop_ka_ero, xlab = "Liikennevalojen lkm", ylab = "Muutos keskinopeudesta (m/s)")
text(4.5,11.5, round(cor(Rist_lv,Nop_ka_ero,method = "pearson"),3))
cor.test(Rist_lv,Nop_ka_ero,method = "spearman") # -0.1225344, p-value < 2.2e-16
cor.test(Rist_lv,Nop_ka_ero,method = "pearson") # -0.1382632, p-value < 2.2e-16

# Segmentin keskinopeuden muutos reitin keskinopeudesta ja autoristeykset
plot(Rist_auto,Nop_ka_ero, xlab = "Liikennevalottomien risteysten lkm", ylab = "Muutos keskinopeudesta (m/s)")
text(4.5,11.5, round(cor(Rist_auto,Nop_ka_ero,method = "pearson"),3))
cor.test(Rist_auto,Nop_ka_ero,method = "spearman") # -0.07990003, p-value < 2.2e-16
cor.test(Rist_auto,Nop_ka_ero,method = "pearson") # -0.08032027, p-value < 2.2e-16

# Segmentin keskinopeuden muutos reitin keskinopeudesta ja kevytristeykset
plot(Rist_kevyt,Nop_ka_ero, xlab = "Kevyen liik. risteysten lkm", ylab = "Muutos keskinopeudesta (m/s)")
text(6.5,11.5, round(cor(Rist_kevyt,Nop_ka_ero,method = "pearson"),3))
cor.test(Rist_kevyt,Nop_ka_ero,method = "spearman") # -0.1365596, p-value < 2.2e-16
cor.test(Rist_kevyt,Nop_ka_ero,method = "pearson") # -0.1537445, p-value < 2.2e-16



## Muutos mediaaninopeuksiin
plot(Gradientti,Nop_md_ero, ylab = "Muutos mediaaninopeudesta (m/s)")
cor.test(Gradientti,Nop_md_ero,method = "spearman") # -0.2937682, p-value < 2.2e-16
cor.test(Gradientti,Nop_md_ero,method = "pearson") # -0.2422213, p-value < 2.2e-16

# Segmentin mediaaninopeuden muutos reitin mediaaninopeudesta ja kaikki risteykset
plot(Rist_yht,Nop_md_ero, xlab = "Risteysten lkm", ylab = "Muutos mediaaninopeudesta (m/s)")
cor.test(Rist_yht,Nop_md_ero,method = "spearman") # -0.1807572, p-value < 2.2e-16
cor.test(Rist_yht,Nop_md_ero,method = "pearson") # -0.2093735, p-value < 2.2e-16

# Segmentin mediaaninopeuden muutos reitin mediaaninopeudesta ja lv-risteykset
plot(Rist_lv,Nop_md_ero, xlab = "Liikennevalojen lkm", ylab = "Muutos mediaaninopeudesta (m/s)")
cor.test(Rist_lv,Nop_md_ero,method = "spearman") # -0.1247304, p-value < 2.2e-16
cor.test(Rist_lv,Nop_md_ero,method = "pearson") # -0.1400585, p-value < 2.2e-16

# Segmentin mediaaninopeuden muutos reitin mediaaninopeudesta ja autoristeykset
plot(Rist_auto,Nop_md_ero, xlab = "Autoristeysten lkm", ylab = "Muutos mediaaninopeudesta (m/s)")
cor.test(Rist_auto,Nop_md_ero,method = "spearman") # -0.07923954, p-value < 2.2e-16
cor.test(Rist_auto,Nop_md_ero,method = "pearson") # -0.07933857, p-value < 2.2e-16

# Segmentin mediaaninopeuden muutos reitin mediaaninopeudesta ja kevytristeykset
plot(Rist_kevyt,Nop_md_ero, xlab = "Kevyen liik. risteysten lkm", ylab = "Muutos mediaaninopeudesta (m/s)")
cor.test(Rist_kevyt,Nop_md_ero,method = "spearman") # -0.1402096, p-value < 2.2e-16
cor.test(Rist_kevyt,Nop_md_ero,method = "pearson") # -0.1579923, p-value < 2.2e-16

## korreloiko gradientti ja risteykset keskenään? (ei pitäisi)
plot(Rist_yht,Gradientti)
cor.test(Rist_yht,Gradientti,method = "spearman") # -0.002629823, p-value = 0.2107
cor.test(Rist_yht,Gradientti,method = "pearson") # -0.00317404, p-value = 0.1309 
# Ei merkitseviä korrelaatioita


## Korreloivatko eri risteystyypit? ##
# liikennevalot ja autoristeykset
plot(Rist_lv,Rist_auto)
cor.test(Rist_lv,Rist_auto,method = "spearman") # -0.0520964, p-value < 2.2e-16
cor.test(Rist_lv,Rist_auto,method = "pearson") # -0.0469375, p-value < 2.2e-16
# merkitsevät, mutta heikot korrelaatiot -> ei ainakaan sen enempää kuin mikään muukaan

# liikennevalot ja kevytristeykset
plot(Rist_lv,Rist_kevyt)
cor.test(Rist_lv,Rist_kevyt,method = "spearman") # 0.09043237, p-value < 2.2e-16 -> korrelaatio muihin nähden aika voimakas, positiivinen?
cor.test(Rist_lv,Rist_kevyt,method = "pearson") # 0.07485408, p-value < 2.2e-16
# auto- ja kevytristeykset
plot(Rist_auto,Rist_kevyt)
cor.test(Rist_auto,Rist_kevyt,method = "spearman") # -0.01767961, p-value < 2.2e-16
cor.test(Rist_auto,Rist_kevyt,method = "pearson") # -0.01364905, p-value = 8.25e-11 


## Pairplot -> monta kuvaajaa samaan kuvaan
myFormula1 = ~ SPEED_mps.x + Gradientti + Rist_lv + Rist_auto + Rist_kevyt + Rist_yht
pairs(myFormula1)




### Lineaarinen regressio ###
# Testaa jotain lineaarista mallia
lm_grad = lm(Nop_ka_ero ~ Gradientti)
summary(lm_grad)
plot(lm_grad)             

# Model validation
res <- resid(lm_grad, type = "pearson")
fit <- fitted(lm_grad)
plot(x = fit, 
     y = res,
     xlab = "Fitted values",
     ylab = "Residuals")      
abline(h = 0, v = 0, lty = 2)

#Normality -> residuaalien normaalisuus
hist(res) # -> histogrammi jokseenkin normaali mutta huipukas


## Kaikki risteykset
lm_rist = lm(Nop_ka_ero ~ Rist_yht)
summary(lm_rist)
plot(lm_rist)

# Residuaalit
res_r <- resid(lm_rist, type = "pearson")
hist(res_r) # -> histogrammi jokseenkin normaali mutta huipukas


## Liikennevalot
lm_lv = lm(Nop_ka_ero ~ Rist_lv)
summary(lm_lv)
#plot(lm_lv)
# Residuaalit
res_lv <- resid(lm_lv, type = "pearson")
hist(res_lv) # -> histogrammi jokseenkin normaali mutta huipukas

## Autoristeykset
lm_auto = lm(Nop_ka_ero ~ Rist_auto)
summary(lm_auto)
# Residuaalit
res_auto <- resid(lm_auto, type = "pearson")
hist(res_auto) # melko normaalin oloinen, aika huipukkaita nämä on kaikki

## Kevytristeykset
lm_kevyt = lm(Nop_ka_ero ~ Rist_lv)
summary(lm_kevyt)
# Residuaalit
res_kevyt <- resid(lm_kevyt, type = "pearson")
hist(res_kevyt) # normaalihko, huipukas


## Kaikki
lm_kaikki = lm(Nop_ka_ero ~ Gradientti + Rist_lv + Rist_auto + Rist_kevyt) # R2 0.11
summary(lm_kaikki)
plot(lm_kaikki)

# Residuaalit
res_k <- resid(lm_kaikki, type = "pearson")
hist(res_k) # melko normaalin näköinen, huipukkuutta


# Gradientti ja rist_yht
lm_g_y = lm(Nop_ka_ero ~ Gradientti + Rist_yht)
summary(lm_g_y)


# Gradientti ja liikennevalot
lm_g_lv = lm(Nop_ka_ero ~ Gradientti + Rist_lv)
summary(lm_g_lv)

# Gradientti ja autoristeykset
lm_g_auto = lm(Nop_ka_ero ~ Gradientti + Rist_auto)
summary(lm_g_auto)

# Gradientti ja kevytristeykset
lm_g_kevyt = lm(Nop_ka_ero ~ Gradientti + Rist_kevyt)
summary(lm_g_kevyt)
plot(lm_g_kevyt) 

## Gradientti + lv + muut risteykset
# lasketaan auto + kevyt
segmentit[,"Rist_muut"] <- Rist_auto + Rist_kevyt

attach(segmentit)

plot(Rist_muut,SPEED_mps.x)
cor.test(Rist_muut,SPEED_mps.x, method = "spearman") # -0.1594566, p-value < 2.2e-16
cor.test(Rist_muut,SPEED_mps.x, method = "pearson") # -0.1692936, p-value < 2.2e-16
plot(Rist_muut,Nop_ka_ero)
cor.test(Rist_muut,Nop_ka_ero, method = "spearman") # -0.1564599, p-value < 2.2e-16
cor.test(Rist_muut,Nop_ka_ero, method = "pearson") # -0.172421, p-value < 2.2e-16

# lm-malli
lm_g_lv_m = lm(Nop_ka_ero ~ Gradientti + Rist_lv + Rist_muut)
summary(lm_g_lv_m)
res_glvm <- resid(lm_g_lv_m, type = "pearson")
hist(res_glvm) # tosi huipukas 

# Gradientti + auto + kevyt
lm_g_a_k = lm(Nop_ka_ero ~ Gradientti + Rist_auto + Rist_kevyt)
summary(lm_g_a_k)

# Gradientti + lv + kevyt
lm_g_lv_k = lm(Nop_ka_ero ~ Gradientti + Rist_lv + Rist_kevyt)
summary(lm_g_lv_k)


# Eri risteystyypit
lm_erist = lm(Nop_ka_ero ~ Rist_lv + Rist_auto + Rist_kevyt)
summary(lm_erist)

# Moottoroidut risteykset
lm_mrist = lm(Nop_ka_ero ~ Rist_lv + Rist_auto)
summary(lm_mrist)



## Keskinopeus ja kaikki
lm_knop = lm(SPEED_mps.x ~ Gradientti + Rist_lv + Rist_auto + Rist_kevyt) # R2 0.09
summary(lm_knop)
plot(lm_knop)
res_knop <- resid(lm_knop, type = "pearson")
hist(res_knop) # melko normaali                     

# Sortataan nopeuden perusteella
nop_sort <- segmentit[order(-SPEED_mps.x),]

## Keskinopeus ja gradientti
lm_nop_g = lm(SPEED_mps.x ~ Gradientti)
summary(lm_nop_g)

## Keskinopeus ja kaikki risteykset
lm_nop_rist = lm(SPEED_mps.x ~ Rist_yht)
summary(lm_nop_rist)

## Keskinopeus ja liikennevalot
lm_nop_lv = lm(SPEED_mps.x ~ Rist_lv)
summary(lm_nop_lv)

## Keskinopeus ja autoristeykset
lm_nop_auto = lm(SPEED_mps.x ~ Rist_auto)
summary(lm_nop_auto)

## Keskinopeus ja kevytristeykset
lm_nop_kevyt = lm(SPEED_mps.x ~ Rist_kevyt)
summary(lm_nop_kevyt)

## Keskinopeus, gradientti
lm_nop_g_r = lm(SPEED_mps.x ~ Gradientti + Rist_yht)
summary(lm_nop_g_r)

## Keskinopeus, gradientti, liikennevalot
lm_nop_g_lv = lm(SPEED_mps.x ~ Gradientti + Rist_lv)
summary(lm_nop_g_lv)

## Keskinopeus, gradientti, liikennevalot, kevytristeykset
lm_nop_g_lv_k = lm(SPEED_mps.x ~ Gradientti + Rist_lv + Rist_kevyt)
summary(lm_nop_g_lv_k)

# Liikennevaloprosentti?    # ei taida toimia...
segmentit[,"lv_pros"] <- (Rist_lv/Rist_yht)
attach(segmentit)
hist(lv_pros)
boxplot(lv_pros)
plot(lv_pros,SPEED_mps.x)
cor(lv_pros,SPEED_mps.x,method = "spearman") # NA


#### Pelkkä ylämäki?
segmentit[,"Upslope"] <- Gradientti
attach(segmentit)
segmentit <- within(segmentit, Upslope[Gradientti < 0] <- NA)
attach(segmentit)

boxplot(Upslope)

# Keskinopeus
plot(Upslope,SPEED_mps.x)
cor.test(Upslope,SPEED_mps.x, method="spearman") # -0.1747717, p-value < 2.2e-16
cor.test(Upslope,SPEED_mps.x, method="pearson") # -0.1532443, p-value < 2.2e-16

# Regressio
lm_up = lm(SPEED_mps.x ~ Upslope)
summary(lm_up)

lm_knop_uprist = lm(SPEED_mps.x ~ Upslope + Rist_yht)
summary(lm_knop_uprist)

lm_knopupkaikki = lm(SPEED_mps.x ~ Upslope + Rist_lv + Rist_auto + Rist_kevyt)
summary(lm_knopupkaikki)


# Nopeuden muutos
plot(Upslope,Nop_ka_ero)
cor.test(Upslope,Nop_ka_ero, method="spearman") # -0.2714853, p-value < 2.2e-16
cor.test(Upslope,Nop_ka_ero, method="pearson") # -0.2189954, p-value < 2.2e-16

lm_noperoup = lm(Nop_ka_ero ~ Upslope)
summary(lm_noperoup)

lm_uprist = lm(Nop_ka_ero ~ Upslope + Rist_yht)
summary(lm_uprist)

lm_upkaikki = lm(Nop_ka_ero ~ Upslope + Rist_lv + Rist_auto + Rist_kevyt)
summary(lm_upkaikki)



#---------------------------------------------------------
# Logaritmimuunnos
# log10 nopeuden muutokselle
log_nopkaero = log10(Nop_ka_ero)
hist(log_nopkaero) # -> tulee ihan vino, huippu oikealla
plot(Gradientti,log_nopkaero) 
cor.test(Gradientti,log_nopkaero, method="spearman") # -0.2285539, p-value < 2.2e-16
# ei parane ja tulkittavuus vaikeutuu
plot(Rist_yht,log_nopkaero) 
cor.test(Rist_yht,log_nopkaero, method="spearman") # -0.03779152, p-value < 2.2e-16 
# -> vielä heikompi kuin ilman muunnosta

# log10 keskinopeuksille
log_nopeus = log10(SPEED_mps.x)
hist(log_nopeus) # -> vino, huippu oikealla
plot(Gradientti,log_nopeus) # ei toimi sen paremmin
cor.test(Gradientti,log_nopeus, method="spearman") # -0.2306587, p-value < 2.2e-16
plot(Rist_yht,log_nopeus) # samaa luokkaa kuin ilman muunnosta
cor.test(Rist_yht,log_nopeus, method="spearman") # -0.1834179, p-value < 2.2e-16

lm_lg_ero = lm(log_nopkaero ~ Gradientti + Rist_lv + Rist_auto + Rist_kevyt)
summary(lm_lg_ero)

lm_lg_nop = lm(log_nopeus ~ Gradientti + Rist_lv + Rist_auto + Rist_kevyt) # EI TOIMI 
summary(lm_lg_nop)


# Neliöjuurimuunnos
# nopeuden erotukselle
sqrt_nopkaero = (Nop_ka_ero)^(1/2)
hist(sqrt_nopkaero) # vasemmalle vino, mutta ei niin pahasti kuin log10
plot(Gradientti,sqrt_nopkaero) # tulee vaan pallo, heikompi korrelaatio kuin ilman muunnosta
cor.test(Gradientti,sqrt_nopkaero, method="spearman") # -0.2285539, p-value < 2.2e-16 
plot(Rist_yht,sqrt_nopkaero) # ihan sama/huonompi kuin ennenkin
cor.test(Rist_yht,sqrt_nopkaero, method="spearman") # -0.03779152, p-value < 2.2e-16

# nopeudelle
sqrt_nopeus = (SPEED_mps.x)^(1/2)
hist(sqrt_nopeus) # ei niin pahasti vino kuin kaikki muut
plot(Gradientti,sqrt_nopeus) 
cor.test(Gradientti,sqrt_nopeus, method="spearman") # -0.2306587, p-value < 2.2e-16
plot(Rist_yht,sqrt_nopeus) # viuhka, tiivistymät nyt keskemmällä, korrelaatio sama
cor.test(Rist_yht,sqrt_nopeus, method="spearman") # -0.1834179, p-value < 2.2e-16

lm_sqrt_ero = lm(sqrt_nopkaero ~ Gradientti + Rist_lv + Rist_auto + Rist_kevyt)
summary(lm_sqrt_ero)

lm_sqrt_nop = lm(sqrt_nopeus ~ Gradientti + Rist_lv + Rist_auto + Rist_kevyt)
summary(lm_sqrt_nop)
plot(lm_sqrt_nop) # residuaalit 2 kuvassa suht norm. näköisiä mutta 1 ja 3 kuvat huonoja


### GLM ###
# Kokeillaan selittää keskinopeuksia    -> RIITTÄÄKÖ PELKKÄ AIC TARKASTELU?

# Pelkkä gradientti
# yritetty gammaa mutta "non-positive values not allowed for the 'gamma' family" ?
# kokeillaan gaussian eli normaalijakauma
glm_nop_grad = glm(SPEED_mps.x ~ Gradientti, family = "gaussian")
summary(glm_nop_grad)

# Risteykset gamma-jakaumalla?
# jälleen "non-positive values not allowed for the 'gamma' family" ??
glm_nop_rist = glm(SPEED_mps.x ~ Rist_yht, family = "Gamma")
summary(glm_nop_rist)

# kokeillaan gaussian
glm_nop_rist_norm = glm(SPEED_mps.x ~ Rist_yht, family ="gaussian")
summary(glm_nop_rist_norm)

# nopeus, gradientti ja rist_yht
glm_nop_g_r = glm(SPEED_mps.x ~ Gradientti + Rist_yht, family = "gaussian")
summary(glm_nop_g_r)

# kaikki
glm_nop_kaikki = glm(SPEED_mps.x ~ Gradientti + Rist_lv + Rist_auto + Rist_kevyt, family = "gaussian")
summary(glm_nop_kaikki)





## ------------------------------------------------------------------------------------------ ##
# Tarkasteluun aika! 
# Lasketaan uusi aika-kenttä, koska gps-pisteiden aggregointiin perustuva aika jokseenkin epäluotettava
# matkaaika = segmentin pituus / segmentin keskinopeudella
segmentit[,"matkaaika"]  <- Seg_pituus/SPEED_mps.x
attach(segmentit)
summary(matkaaika)

nop_sort = segmentit[order(SPEED_mps.x),]


# kirjoitetaan csv:ksi
write.csv(nop_sort, "Segmentit_nopsort.csv", row.names=FALSE)

# poistettu 0-arvot käsin

# luetaan sisään erilliseen skriptiin: Segmenttien_analyysi_aika.R


## -------------------------------------------------------------------------------------------
# Väylätyypin vaikutus
# Korjataan HLEVEL 8 & 18 -> pyoravayla 1
segmentit <- within(segmentit, Pyoravayla[H_LEVEL == 8] <- 1)
segmentit <- within(segmentit, Pyoravayla[H_LEVEL == 18] <- 1)

hist(Tieluokitus)
hist(Pyoravayla)

# Laitetaan tieluokitukseen 3, jos kyseessä on pyöräväylä (korvaa siis olemassa olevia kakkosia)
segmentit <- within(segmentit, Tieluokitus[Pyoravayla == 1] <- 3)
# 1 = Autotie
# 2 = Kevyen liikenteen väylä (muu kuin jalkakäytävä)
# 3 = Pyöräväylä
# 9 = Pyöräilyltä kielletty 
attach(segmentit)
summary(segmentit)

hist(Tieluokitus)

# mediaaninopeudet boxplotista
boxplot(SPEED_mps.x ~ Tieluokitus, xlab="Tieluokitus",ylab="Keskinopeus (m/s)")
boxplot(SPEED_mps.x ~ Tieluokitus, plot=FALSE)

# Regressiomalleja pyöräväylä-muuttujalle
# Keskinopeus
lm_knop_vayla = lm(SPEED_mps.x ~ Pyoravayla)
summary(lm_knop_vayla)

# Pyöräväylä mukaan kaiken yhdistävään malliin
lm_knop_kaikki_vayla = lm(SPEED_mps.x ~ Gradientti + Rist_lv + Rist_auto +Rist_kevyt + Pyoravayla)
summary(lm_knop_kaikki_vayla)

# Eri risteykset ja pyöräväylä
lm_knop_eristvayla = lm(SPEED_mps.x ~ Rist_lv + Rist_auto +Rist_kevyt + Pyoravayla)
summary(lm_knop_eristvayla)

lm_rist_vayla = lm(SPEED_mps.x ~ Rist_yht + Pyoravayla)
summary(lm_rist_vayla)

lm_grad_vayla = lm(SPEED_mps.x ~ Gradientti + Pyoravayla)
summary(lm_grad_vayla)

# Nopeuden muutos
lm_vayla = lm(Nop_ka_ero ~ Pyoravayla)
summary(lm_vayla)

lm_kaikki_vayla = lm(Nop_ka_ero ~ Gradientti + Rist_lv + Rist_auto + Rist_kevyt + Pyoravayla)
summary(lm_kaikki_vayla)

lm_erist_vayla = lm(Nop_ka_ero ~ Rist_lv + Rist_auto + Rist_kevyt + Pyoravayla)
summary(lm_erist_vayla) # R2 = 0,1089

lm_grad_vayla2 = lm(Nop_ka_ero ~ Gradientti + Pyoravayla)
summary(lm_grad_vayla2)

lm_gr_rist_vayla = lm(Nop_ka_ero ~ Gradientti + Rist_yht + Pyoravayla)
summary(lm_gr_rist_vayla) # R2 0.1036


