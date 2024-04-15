import pandas as pd
from TCSP import read_stopwords_list # traditional chinese stop words
from snownlp import SnowNLP # chinese NLP
from sklearn import pipeline, model_selection
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

class MachineLearning:
    def __init__(self, csv_in):
        self.csv_in = csv_in # path of csv, assume follows fixed structure

def preprocessing(self):
    '''
        This method will carry out data preprocessing and return the processed DataFrame.
        Also, this return y_test and y_pred for further metrics calculations.
    '''
    # Open scrapped content 
    df = pd.read_csv(self.csv_in, header=None)
    df.columns=["index", "link", "title", "comment_date", "comment","n_A", "label","made_by"]
    df.drop(["n_A", "made_by"], axis=1, inplace=True)

    # Stop word removal
    processed_comments = []
    for comment in df["comment"]:
      if comment != "":
        tokens = SnowNLP(comment).words # tokenisation
        processed_comment = ""
        for token in tokens:
          if token not in read_stopwords_list(): # stop word removal
            processed_comment += token
      else:
        processed_comment = ""
      processed_comments.append(processed_comment)
    df["processed_comment"] = processed_comments

    # add column of sentiment analysis score of comment
    sentiments = []
    for comment in df["processed_comment"]:
      if comment != "":
        sentiment = SnowNLP(comment).sentiments
      else:
        sentiment = 0
      sentiments.append(sentiment)
    df["sentiment"] = sentiments
    df['label'].replace({'No': 0, 'Yes': 1}, inplace=True) # turn yes to 1 and no to 0
  
    return df

def train(self, df):
    '''
        This method will conduct machine learning stage with the processed DataFrame, df.
    '''
    ## Model training
    data = pd.DataFrame({"title": df["title"], "processed_comment": df["processed_comment"], "sentiment": df["sentiment"], "label": df["label"]})
    X = data[["title", "processed_comment", "sentiment"]]
    #print(X.head())
    Y = data["label"]

    # get an 80-20 test-train split
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, Y, test_size=0.2, random_state=45)

    #print(X_train.shape)
    #print(y_train.shape)

    # Transformers
    tfid = TfidfVectorizer()
    scaler = StandardScaler()
    x_transformer = ColumnTransformer([
        ('title', tfid, "title"),
        ('processed_comment', tfid, "processed_comment"),
        ('sentiment', scaler, ["sentiment"]),
    ])
    # Pipelines
    pipe = pipeline.Pipeline([
        ('input', x_transformer),
        ('clf', SVC()),
    ])
    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)
    
    return y_test, y_pred

def performance(self, y_test, y_pred):
    print("Classification Report:\n", classification_report(y_test, y_pred))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    cm_display = ConfusionMatrixDisplay(confusion_matrix = confusion_matrix(y_test, y_pred), display_labels = [False, True])
    cm_display.plot()
    plt.show()