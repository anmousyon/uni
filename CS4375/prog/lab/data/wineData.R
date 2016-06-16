d=read.csv("https://archive.ics.uci.edu/ml/machine-learning-databases/wine/wine.data", header = F)
names(d)<- c("Class", "Alcohol", "Malic acid", "Ash", "Alcalinity of ash", "Magnesium", 
             "Total phenols", "Flavanoids", "Nonflavanoid phenols", "Proanthocyanins", "Color intensity"
              ,"Hue", "OD280/OD315 of diluted wines", "Proline")            

