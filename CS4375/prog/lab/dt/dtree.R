library(rpart)
#to look at data
stagec
# to summarize data
stagec
progstat <- factor(stagec$pgstat, levels = 0:1, labels = c("No", "Prog"))
cfit  <- rpart(progstat ~  age + eet + g2 + grade + gleason + ploidy, data = stagec, method ='class')
print(cfit)
par(mar = rep(0.1, 4))
plot(cfit)
text(cfit)
printcp(cfit)
summary(cfit, cp = 0.06)



library("party")
str(iris)
iris_ctree <- ctree(Species ~ Sepal.Length + Sepal.Width + Petal.Length + Petal.Width, data=iris)
print(iris_ctree)
plot(iris_ctree)
plot(iris_ctree, type="simple")


fit <- rpart(Kyphosis ~ Age + Number + Start, data = kyphosis)
fit2 <- rpart(Kyphosis ~ Age + Number + Start, data = kyphosis,
              parms = list(prior = c(.65,.35), split = "information"))
fit3 <- rpart(Kyphosis ~ Age + Number + Start, data = kyphosis,
              control = rpart.control(cp = 0.05))
par(mfrow = c(1,2), xpd = NA) # otherwise on some devices the text is clipped
plot(fit)
text(fit, use.n = TRUE)
plot(fit2)
text(fit2, use.n = TRUE)


