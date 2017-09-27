# Tarkasteluja matka-ajan suhteen
rm(list=ls())

setwd("fp")
table = ("Segmentit_nollat_pois_edit.csv")
nollat_pois = read.csv(table, header = TRUE)

attach(nollat_pois)
summary(nollat_pois)



# Tutkitaan muuttuiko muut arvot nollien poistolla
# segmentin keskinopeus
boxplot(SPEED_mps.x, main = "Segmentin keskinopeus (m/s)", horizontal = TRUE) 
dotchart(SPEED_mps.x, main = "Segmentin keskinopeus (m/s)",
         xlab = "Range of data", 
         ylab = "Order of the data")

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
qqline(Gradientti, col = "red") # ei normaali muttei tarvitsekaan olla

# lasketaan matka-aika (segmentin pituus / keskinopeus)
nollat_pois[,"matkaaika"]  <- Seg_pituus/SPEED_mps.x
attach(nollat_pois)
summary(matkaaika)


boxplot(matkaaika, main = "Aika (s)", horizontal = TRUE)
dotchart(matkaaika, main = "Aika (s)")
hist(matkaaika) 
qqnorm(matkaaika)
qqline(matkaaika, col = "red")

# Kaikki risteykset
boxplot(Rist_yht, main = "Risteysten lkm", horizontal = TRUE)
dotchart(Rist_yht, main = "Risteysten lkm")
hist(Rist_yht)


## Korrelaatiot ##

# Gradientti ja aika 
plot(Gradientti,matkaaika, xlab="Gradientti (%)", ylab="Matka-aika (s)")
cor.test(Gradientti,matkaaika,method = "spearman") # 0.2302577, p-value < 2.2e-16
cor.test(Gradientti,matkaaika,method = "pearson") # 0.1310992, p-value < 2.2e-16
text(20,200, round(cor(Gradientti,matkaaika,method = "spearman"),3))

# Kaikki risteykset ja aika
plot(Rist_yht,matkaaika, xlab="Risteysten lkm", ylab="Matka-aika (s)")
cor.test(Rist_yht,matkaaika,method = "spearman") # 0.1838991, p-value < 2.2e-16
cor.test(Rist_yht,matkaaika,method = "pearson") # 0.1973214, p-value < 2.2e-16
text(6,250, round(cor(Rist_yht,matkaaika,method = "spearman"),3))
# käy tekemässä lm-malli (alempana) sitten abline!
abline(lm_a_rist)

# Liikennevalot ja aika
plot(Rist_lv,matkaaika, xlab="Liikennevalojen lkm", ylab="Matka-aika (s)")
cor.test(Rist_lv,matkaaika,method = "spearman") # 0.1319466, p-value < 2.2e-16
cor.test(Rist_lv,matkaaika,method = "pearson") # 0.1671045
text(4,250, round(cor(Rist_lv,matkaaika,method = "spearman"),3))

# Autoristeykset ja aika
plot(Rist_auto,matkaaika)
cor(Rist_auto,matkaaika,method = "spearman") # 0.06936944
cor(Rist_auto,matkaaika,method = "pearson") # 0.05541936

# Kevyen liikenteen risteykset ja aika
plot(Rist_kevyt,matkaaika)
cor(Rist_kevyt,matkaaika,method = "spearman") # 0.1495204
cor(Rist_kevyt,matkaaika,method = "pearson") # 0.1482393


## Lineaarinen regressio ##
# Aika ja gradientti
lm_a_g = lm(matkaaika ~ Gradientti)
summary(lm_a_g)


# Aika ja kaikki risteykset
lm_a_rist  = lm(matkaaika ~ Rist_yht)
summary(lm_a_rist)

# Aika, gradientti, ja kaikki risteykset
lm_a_g_rist = lm(matkaaika ~ Gradientti + Rist_yht)
summary(lm_a_g_rist)


