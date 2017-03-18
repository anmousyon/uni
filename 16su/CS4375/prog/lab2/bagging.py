'''bagging classifier lab'''
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_iris
from sklearn.cross_validation import train_test_split

def main():
    '''main function'''
    bagging = BaggingClassifier(DecisionTreeClassifier())
    iris = load_iris()
    x = iris.data
    y = iris.target
    #train, test, train_, test_ = train_test_split(x, y, test_size=0.2, random_state=42)
    bagging.fit(x, y)
    bagging.predict(x[:2])
    print(bagging.score(x[:2], y[:2]))

main()
