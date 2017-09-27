# Validointireittien analyysi

rm(list=ls()) #Clear all data

setwd("fp")

taulukko = "Validointireitit.txt"
validointireitit = read.csv(taulukko, header = TRUE, sep = ";")
attach(validointireitit)

sorted <- validointireitit[order(FIRST_CycID),]

# Valitaan kaikki paitsi ID 16
newdata <- sorted[ which(sorted$FIRST_CycID != 16),]

# Tyypin 4 pyöräilijät

hist(newdata$SUM_Aika4)
hist(newdata$DURATION_mins)
hist(newdata$SUM_Aika4hidaste)

# Plotataan GPS-aineisto ja vakionopeuden malli
plot(newdata$SUM_Aika4,newdata$DURATION_mins, xlab="Vakionopeuden malli",ylab="GPS-aineisto",main = "Matka-aika minuutteina")
text(87,75, round(cor(newdata$SUM_Aika4,newdata$DURATION_mins, method = "spearman"),3))
cor.test(newdata$SUM_Aika4,newdata$DURATION_mins,method = "spearman") # rho=0.9473065, R2 = 0.8973896, p-value < 2.2e-16
cor.test(newdata$SUM_Aika4,newdata$DURATION_mins,method = "pearson") # r=0.9231639, R2 = 0.8522316, p-value < 2.2e-16

# Plotataan GPS-aineisto ja hidastemalli
plot(newdata$SUM_Aika4hidaste,newdata$DURATION_mins, xlab="Vakionopeuden malli hidasteella",ylab="GPS-aineisto",main = "Matka-aika minuutteina")
text(87,75, round(cor(newdata$SUM_Aika4hidaste,newdata$DURATION_mins, method = "spearman"),3))
cor.test(newdata$SUM_Aika4hidaste,newdata$DURATION_mins,method = "spearman") # rho=0.9501278, R2 = 0.9027428, p-value < 2.2e-16
cor.test(newdata$SUM_Aika4hidaste,newdata$DURATION_mins,method = "pearson") # r=0.9260449, R2 = 0.8575592, p-value < 2.2e-16

# Tyypin 5 pyöräilijä
cyc5 <- sorted[ which(sorted$FIRST_CycID == 16),]

hist(cyc5$SUM_Aika5)
hist(cyc5$DURATION_mins)
hist(cyc5$SUM_Aika5hidaste)

# Plotataan GPS-aineisto ja vakionopeuden malli
plot(cyc5$SUM_Aika5,cyc5$DURATION_mins, xlab="Vakionopeuden malli",ylab="GPS-aineisto",main = "Matka-aika minuutteina")
text(43,38, round(cor(cyc5$SUM_Aika5,cyc5$DURATION_mins, method = "spearman"),3))
cor.test(cyc5$SUM_Aika5,cyc5$DURATION_mins,method = "spearman") # rho=0.9880065, R2 = 0.9761568, p-value < 2.2e-16
cor.test(cyc5$SUM_Aika5,cyc5$DURATION_mins,method = "pearson") # r=0.9919048, R2 = 0.9838751, p-value < 2.2e-16

# Plotataan GPS-aineisto ja hidastemalli
plot(cyc5$SUM_Aika5hidaste,cyc5$DURATION_mins, xlab="Vakionopeuden malli hidasteella",ylab="GPS-aineisto",main = "Matka-aika minuutteina")
text(43,38, round(cor(cyc5$SUM_Aika5hidaste,cyc5$DURATION_mins, method = "spearman"),3))
cor.test(cyc5$SUM_Aika5hidaste,cyc5$DURATION_mins,method = "spearman") # rho=0.9874392, R2 = 0.9750362, p-value < 2.2e-16
cor.test(cyc5$SUM_Aika5hidaste,cyc5$DURATION_mins,method = "pearson") # r=0.9925113, R2 = 0.9850787, p-value < 2.2e-16

# Kaikki data yhdessä
# lisätään kenttä
sorted[,"Aika_kaikki"] <- 0
sorted[,"Aikahidaste_kaikki"] <- 0

attach(sorted)

# Annetaan pyöräilijätyyppiä vastaava nopeusarvo
sorted <- within(sorted, Aika_kaikki[FIRST_CycID == 16] <- sorted[which(FIRST_CycID == 16),"SUM_Aika5"])
sorted <- within(sorted, Aikahidaste_kaikki[FIRST_CycID == 16] <- sorted[which(FIRST_CycID == 16),"SUM_Aika5hidaste"])
sorted <- within(sorted, Aika_kaikki[FIRST_CycID != 16] <- sorted[which(FIRST_CycID != 16),"SUM_Aika4"])
sorted <- within(sorted, Aikahidaste_kaikki[FIRST_CycID != 16] <- sorted[which(FIRST_CycID != 16),"SUM_Aika4hidaste"])

attach(sorted)

# Plotataan GPS-aineisto ja vakionopeuden malli
plot(Aika_kaikki,DURATION_mins,xlab="Vakionopeuden malli",ylab="GPS-aineisto",main = "Matka-aika minuutteina")
text(87,75, round(cor(Aika_kaikki,DURATION_mins, method = "spearman"),3))
cor.test(Aika_kaikki,DURATION_mins,method = "spearman") # rho=0.9553509, R2 = 0.9126953, p-value < 2.2e-16
cor.test(Aika_kaikki,DURATION_mins,method = "pearson") # r=0.9311607, R2 = 0.8670602, p-value < 2.2e-16

# Plotataan GPS-aineisto ja hidastemalli
plot(Aikahidaste_kaikki,DURATION_mins,xlab="Vakionopeuden malli hidasteella",ylab="GPS-aineisto",main = "Matka-aika minuutteina")
text(87,75, round(cor(Aikahidaste_kaikki,DURATION_mins, method = "spearman"),3))
cor.test(Aikahidaste_kaikki,DURATION_mins,method = "spearman") # rho=0.9575635, R2 = 0.9169279, p-value < 2.2e-16
cor.test(Aikahidaste_kaikki,DURATION_mins,method = "pearson") # r=0.933747, R2 = 0.8718835, p-value < 2.2e-16


