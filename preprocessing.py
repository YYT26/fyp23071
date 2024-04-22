import pandas as pd
from TCSP import read_stopwords_list # traditional chinese stop words
from snownlp import SnowNLP # chinese NLP

df = pd.read_csv("data (1).csv")
df.columns=["index", "link", "title", "comment_date", "comment","n_A", "label","made_by"] # df structure

## remove unecessary columns
df.drop(["n_A", "made_by"], axis=1, inplace=True)

# comment_date: replace na values with value after
df["comment_date"].fillna(method="bfill", inplace=True)

# comment_date: transform data type to datetime
df["comment_date"] = pd.to_datetime(df["comment_date"].apply(lambda x: x[0:x.find(" ")-1].replace("年", "-").replace("月", "-")), format="%Y-%m-%d")

# Label bank based on title
df_result = pd.read_csv("data_scaped/LIHKG_News_all_results(1).csv")
df_title={"title":[],
          "bank":[]}
for i in df['title'].drop_duplicates():
    match = df_result[i==df_result["title"]]
    if len(set(match["bank"]))==1:
        df_title["title"].append(i)
        df_title["bank"].append(match["bank"].values[0])
    elif len(set(match["bank"]))>1:
        df_title["title"].append(i)
        df_title["bank"].append(list(set(match["bank"])))
    else:
        print(i)
df_title = pd.DataFrame(df_title)
df["bank"] = df["title"].apply(lambda x: df_title[df_title["title"]==x]["bank"].values[0])

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

# Turn "Yes" to 1 and "No" to 0
df['label'].replace({'No': 0, 'Yes': 1}, inplace=True) # turn yes to 1 and no to 0

# output the processed data into csv, for shorter loading time in streamlit
df.to_csv("processed_data.csv", index=False)