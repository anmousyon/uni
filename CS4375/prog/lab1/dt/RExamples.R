# uncomment if you want to install
install.packages("rpart", dependencies=TRUE)
library(rpart)
progstat <- factor(stagec$pgstat, levels = 0:1, labels = c("No", "Prog"))
cfit  <- rpart(progstat ~  age + eet + g2 + grade + gleason + ploidy, parms = list(split = 'information'), 
               data = stagec, method = 'class')
print(cfit)
par(mar = rep(0.1, 4))
plot(cfit)
text(cfit)
print(cfit)
summary(cfit)

##########################################
# Pruning the tree
#########################################
printcp(cfit)
prunedTree <- prune(cfit, cp = 0.010000)

##########################################
# Find predictions
#########################################

z.auto <- rpart(Mileage ~ Weight, car.test.frame)
predict(z.auto)

fit <- rpart(Kyphosis ~ Age + Number + Start, data = kyphosis)
predict(fit, type = "prob")   # class probabilities (default)
predict(fit, type = "vector") # level numbers
predict(fit, type = "class")  # factor
predict(fit, type = "matrix") # level number, class frequencies, probabilities

sub <- c(sample(1:50, 25), sample(51:100, 25), sample(101:150, 25))
fit <- rpart(Species ~ ., data = iris, subset = sub)
fit
table(predict(fit, iris[-sub,], type = "class"), iris[-sub, "Species"])



##########################################
# Car dataset cu.summary
#########################################
fit1 <- rpart(Reliability ~ Price + Country + Mileage + Type,
              data = cu.summary, parms = list(split =
                                                'gini'
              ))
fit2 <- rpart(Reliability ~ Price + Country + Mileage + Type,
              data = cu.summary, parms = list(split =
                                                'information'
              ))
par(mfrow = c(1,2), mar = rep(0.1, 4))
plot(fit1, margin = 0.05); text(fit1, use.n = TRUE, cex = 0.8)
plot(fit2, margin = 0.05); text(fit2, use.n = TRUE, cex = 0.8)
summary(fit1, cp = 0.06)