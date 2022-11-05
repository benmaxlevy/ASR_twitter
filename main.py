import pandas as pd

from imblearn.over_sampling import RandomOverSampler

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

from sklearn import metrics
from sklearn.metrics import PrecisionRecallDisplay


def train():
    vectorizer = CountVectorizer()

    col_names = ["text", "label"]
    df = pd.read_csv("datasets/twitter_dataset.csv")

    X = vectorizer.fit_transform(df["text"])
    y = df["label"]

    ros = RandomOverSampler(random_state=16)
    X, y = ros.fit_resample(X, y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=16)

    clf = LogisticRegression()
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    print(metrics.confusion_matrix(y_test, y_pred, labels=["suicidal", "normal"]))
    print(metrics.classification_report(y_test, y_pred, labels=["suicidal", "normal"]))
    # display = PrecisionRecallDisplay.from_estimator(
    #     logreg, X_test, y_test, name="LogReg"
    # )
    # _ = display.ax_.set_title("2-class Precision-Recall curve")
    return clf, vectorizer


def classify(text, clf, vectorizer):
    X = vectorizer.transform(text)
    return clf.predict(X)


def main():
    trained_clf, fitted_vectorizer = train()
    print(classify(["fuck my life", "just end it all", "kill me", "i wanna kill myself",
                    "that was the worst day of my life - i wanna die", "i'm suicidal"], trained_clf, fitted_vectorizer))


if __name__ == "__main__":
    main()
