# Reittikohtainen tarkastelu

# aggregoidaan takaisin reiteiksi segmentit, joista on poistettu virheelliset joinit
rm(list=ls())

setwd("fp")
table = ("Segmentit_kaikki_editoitu.csv")
segmentit_edit = read.csv(table, header = TRUE, sep=",")

attach(segmentit_edit)
summary(segmentit_edit)

# Aggregoidaan reiteiksi nimen perusteella ja lasketaan uudelleen tunnuslukuja
reitit = aggregate(SPEED_mps.x ~ Nimi, segmentit_edit, mean)

# nopeuden mediaani
nop_md = aggregate(Speed_md ~ Nimi, segmentit_edit, median)
# Gradientin maksimi
grad_max = aggregate(Gradientti ~ Nimi, segmentit_edit, max)
# Gradientin minimi
grad_min = aggregate(Gradientti ~ Nimi, segmentit_edit, min)
# Gradientin keskiarvo
grad_mean = aggregate(Gradientti ~ Nimi, segmentit_edit, mean)
# Gradientin mediaani
grad_md = aggregate(Gradientti ~ Nimi, segmentit_edit, median)
# Kaikki risteykset yhteens?
risteykset = aggregate(Rist_yht ~ Nimi, segmentit_edit, sum)
# Liikennevalot
lv = aggregate(Rist_lv ~ Nimi, segmentit_edit, sum)
# Autoristeykset 
auto = aggregate(Rist_auto ~ Nimi, segmentit_edit, sum)
# Kevyt liikenne
kevyt = aggregate(Rist_kevyt ~ Nimi, segmentit_edit, sum)
# Reitin pituus
reittipituus = aggregate(Reittipituus ~ Nimi, segmentit_edit, median)
# Aika
reittiaika = aggregate(aika ~ Nimi, segmentit_edit, sum)
# GPS count
gpscount = aggregate(Count_gps ~ Nimi, segmentit_edit, sum)


# Lis‰t‰‰n kent‰t samaan dataframeen
reitit[,"Speed_md"] <- nop_md[,"Speed_md"]
reitit[,"Grad_max"] <- grad_max[,"Gradientti"]
reitit[,"Grad_min"] <- grad_min[,"Gradientti"]
reitit[,"Grad_mean"] <- grad_mean[,"Gradientti"]
reitit[,"Grad_md"] <- grad_md[,"Gradientti"]
reitit[,"Rist_yht"] <- risteykset[,"Rist_yht"]
reitit[,"Rist_lv"] <- lv[,"Rist_lv"]
reitit[,"Rist_auto"] <- auto[,"Rist_auto"]
reitit[,"Rist_kevyt"] <- kevyt[,"Rist_kevyt"]
reitit[,"Reittipituus"] <- reittipituus[,"Reittipituus"]
reitit[,"aika"] <- reittiaika[,"aika"]
reitit[,"Count_gps"] <- gpscount[,"Count_gps"]

# Lasketaan liikennevaloprosentti
reitit[,"lv_pros"] <- (reitit$Rist_lv / reitit$Rist_yht)

# kirjoitetaan tiedosto
write.csv(reitit, "Reitit.csv", row.names=FALSE)

###################################################
rm(list=ls())
setwd("fp")
# Luetaan reittitiedosto
table2 = ("Reitit.csv")
Reitit = read.csv(table2, header = TRUE, sep=",")

attach(Reitit)
summary(Reitit)

# Reittien keskinopeus
boxplot(SPEED_mps.x, main = "Reittien keskinopeus (m/s)", horizontal = TRUE) 
hist(SPEED_mps.x)

# Gradientin keskiarvo
boxplot(Grad_mean, horizontal = TRUE)
hist(Grad_mean)

# Gradientin mediaani
boxplot(Grad_md, horizontal=TRUE)
hist(Grad_md)

# Maksimigradientti
boxplot(Grad_max, horizontal = TRUE)
hist(Grad_max)

# Minimigradientti
boxplot(Grad_min, horizontal = TRUE)
hist(Grad_min)

# Reittien pituus
hist(Reittipituus)

# Aika
hist(aika)


## Scatterplotteja ##
# Aika ja reitin pituus
plot(Reittipituus, aika, xlab="Reitin pituus (m)", ylab="Aika (s)")
cor.test(Reittipituus, aika, method="spearman") # 0.9537424, p-value < 2.2e-16
cor.test(Reittipituus, aika, method="pearson") # 0.9436807, p-value < 2.2e-16

# Nopeus ja reitin pituus
plot(Reittipituus, SPEED_mps.x, xlab="Reitin pituus (m)", ylab="Reitin keskinopeus (m/s)")
cor.test(Reittipituus, SPEED_mps.x, method="spearman") # 0.3179433, p-value < 2.2e-16
cor.test(Reittipituus, SPEED_mps.x, method="pearson") # 0.3086846, p-value < 2.2e-16

# Nopeus ja maksimigradientti
plot(Grad_max, SPEED_mps.x, xlab="Maksimigradientti (%)", ylab="Reitin keskinopeus (m/s)")
text(25,10, round(cor(Grad_max,SPEED_mps.x,method = "pearson"),3))
cor.test(Grad_max, SPEED_mps.x, method="spearman") # 0.2066202, p-value = 2.793e-14
cor.test(Grad_max, SPEED_mps.x, method="pearson") # 0.2105652, p-value = 8.882e-15

# Nopeus ja minimigradientti
plot(Grad_min, SPEED_mps.x, xlab="Minimigradientti (%)", ylab="Reitin keskinopeus (m/s)")
cor.test(Grad_min, SPEED_mps.x, method="spearman") # -0.2235777, < 2.2e-16
cor.test(Grad_min, SPEED_mps.x, method="pearson") # -0.2227734, < 2.2e-16

# Nopeus ja risteysten m‰‰r‰ -> positiivinen korrelaatio?
plot(Rist_yht, SPEED_mps.x, xlab="Risteysten lkm", ylab="Reitin keskinopeus (m/s)")
text(600,10, round(cor(Rist_yht,SPEED_mps.x,method = "pearson"),3))
cor.test(Rist_yht, SPEED_mps.x, method="spearman") # 0.2301008, p-value < 2.2e-16
cor.test(Rist_yht, SPEED_mps.x, method="pearson") # 0.2316227, p-value < 2.2e-16

# Nopeus ja liikennevalojen m‰‰r‰
plot(Rist_lv, SPEED_mps.x, xlab="Liikennevalojen lkm", ylab="Reitin keskinopeus (m/s)")
text(70,10, round(cor(Rist_lv,SPEED_mps.x,method = "pearson"),3))
cor.test(Rist_lv, SPEED_mps.x, method="spearman") # 0.0145425, p-value = 0.5963 -> ei merkitsev?!
cor.test(Rist_lv, SPEED_mps.x, method="pearson") # 0.0350687, p-value = 0.2014 -> ei merkitsev?!

# Nopeus ja liikennevaloprosentti
plot(lv_pros, SPEED_mps.x, xlab="Liikennevalo%", ylab="Reitin keskinopeus (m/s)")
text(0.7,10, round(cor(lv_pros,SPEED_mps.x,method = "pearson"),3))
cor.test(lv_pros, SPEED_mps.x, method="spearman") # -0.1915207, p-value = 1.913e-12
cor.test(lv_pros, SPEED_mps.x, method="pearson") # -0.2055537, p-value = 3.806e-14

# regressio
Rlm_lvpros = lm(SPEED_mps.x ~ lv_pros)
summary(Rlm_lvpros)

# Nopeus ja autoristeykset -> positiivinen korrelaatio?
plot(Rist_auto, SPEED_mps.x, xlab="Liikennevalottomien risteysten lkm", ylab="Reitin keskinopeus (m/s)")
text(200,10, round(cor(Rist_auto,SPEED_mps.x,method = "pearson"),3))
cor.test(Rist_auto, SPEED_mps.x, method="spearman") # 0.2494087, p-value < 2.2e-16
cor.test(Rist_auto, SPEED_mps.x, method="pearson") # 0.2675315, p-value < 2.2e-16

# Nopeus ja kevytristeykset -> positiivinen korrelaatio
plot(Rist_kevyt, SPEED_mps.x, xlab="Kevyen liik. risteysten lkm", ylab="Reitin keskinopeus (m/s)")
text(200,10, round(cor(Rist_kevyt,SPEED_mps.x,method = "pearson"),3))
cor.test(Rist_kevyt, SPEED_mps.x, method="spearman") # 0.2177282, p-value = 1.004e-15
cor.test(Rist_kevyt, SPEED_mps.x, method="pearson") # 0.1917615, p-value = 1.793e-12

# Lasketaan risteysten lkm/km
Reitit[,"Rist_km"] <- (Rist_yht/Reittipituus*1000)
# lkm/km risteystyypeitt?in
Reitit[,"LV_km"] <- (Rist_lv/Reittipituus*1000)
Reitit[,"Auto_km"] <- (Rist_auto/Reittipituus*1000)
Reitit[,"Kevyt_km"] <- (Rist_kevyt/Reittipituus*1000)
attach(Reitit)

# Lasketaan pelkk‰ upslope, eli kentt‰ average slopesta -> NA negatiivisille gradienteille
Reitit[,"Upslope"] <- Grad_mean
#Reitit[,"Upslope"] <- NULL
attach(Reitit)
Reitit <- within(Reitit, Upslope[Grad_mean < 0] <- NA)
attach(Reitit)



# Plotataan
# Kaikki risteykset / km
plot(Rist_km, SPEED_mps.x, xlab="Risteyksi‰ / km", ylab="Reitin keskinopeus (m/s)")
text(45,10, round(cor(Rist_km,SPEED_mps.x,method = "pearson"),3))
cor.test(Rist_km, SPEED_mps.x, method="spearman") # -0.3778439, p-value < 2.2e-16
cor.test(Rist_km, SPEED_mps.x, method="pearson") # -0.3528259, p-value < 2.2e-16

Rlm_ristkm = lm(SPEED_mps.x ~ Rist_km)
summary(Rlm_ristkm)

# Liikennevalot/km
plot(LV_km, SPEED_mps.x, xlab="Liikennevaloja / km", ylab="Reitin keskinopeus (m/s)")
text(17,10, round(cor(LV_km,SPEED_mps.x,method = "pearson"),3))
cor.test(LV_km, SPEED_mps.x, method="spearman") # -0.2383054, p-value < 2.2e-16
cor.test(LV_km, SPEED_mps.x, method="pearson") # -0.2403613, p-value < 2.2e-16

Rlm_lvkm = lm(SPEED_mps.x ~ LV_km)
summary(Rlm_lvkm)

# Autoristeykset/km
plot(Auto_km, SPEED_mps.x, xlab="Liikennevalottomia risteyksi‰ / km", ylab="Reitin keskinopeus (m/s)")
text(20,10, round(cor(Auto_km,SPEED_mps.x,method = "pearson"),3))
cor.test(Auto_km, SPEED_mps.x, method="spearman") # -0.1138576, p-value = 3.177e-05
cor.test(Auto_km, SPEED_mps.x, method="pearson") # -0.1414797, p-value = 2.232e-07

Rlm_autokm = lm(SPEED_mps.x ~ Auto_km)
summary(Rlm_autokm)

# Kevyen liikenteen risteykset / km
plot(Kevyt_km, SPEED_mps.x, xlab="Kevyen liikenteen risteyksi‰ / km", ylab="Reitin keskinopeus (m/s)")
text(47,10, round(cor(Kevyt_km,SPEED_mps.x,method = "pearson"),3))
cor.test(Kevyt_km, SPEED_mps.x, method="spearman") # -0.1896868, p-value = 3.125e-12
cor.test(Kevyt_km, SPEED_mps.x, method="pearson") # -0.199898, p-value = 1.911e-13

Rlm_kevytkm = lm(SPEED_mps.x ~ Kevyt_km)
summary(Rlm_kevytkm)


# Nopeus ja maksimi-gradientti
Rlm_gmax = lm(SPEED_mps.x ~ Grad_max)
summary(Rlm_gmax)

# Nopeus ja kaikki
Rlm_kaikki = lm(SPEED_mps.x ~ Grad_max + LV_km + Auto_km + Kevyt_km)
summary(Rlm_kaikki)

# Nopeus ja eri risteykset
Rlm_erist = lm(SPEED_mps.x ~ LV_km + Auto_km + Kevyt_km)
summary(Rlm_erist)

# Upslope
plot(Upslope,SPEED_mps.x, xlab="Keskim‰‰r‰inen yl‰m‰kigradientti (%)", ylab="Reitin keskinopeus (m/s)")
text(3.1,10, round(cor(Upslope,SPEED_mps.x, method = "pearson"),3))
cor.test(Upslope,SPEED_mps.x, method="spearman") # -0.169152, p-value = 1.088e-05
cor.test(Upslope,SPEED_mps.x, method="pearson") # -0.2409169, p-value = 2.576e-10


# Samaan kuvaan
par(mfrow=c(2,2))
plot(Rist_km, SPEED_mps.x, xlab="Risteyksi‰ / km", ylab="Keskinopeus (m/s)")
plot(LV_km, SPEED_mps.x, xlab="Liikennevaloja / km", ylab="Keskinopeus (m/s)")
plot(Auto_km, SPEED_mps.x, xlab="Liikennevalottomia risteyksi‰ / km", ylab="Keskinopeus (m/s)")
plot(Kevyt_km, SPEED_mps.x, xlab="Kevyen liikenteen risteyksi‰ / km", ylab="Keskinopeus (m/s)")


# plotit takaisin yhdeksi kuvaksi
par(mfrow=c(1,1))
