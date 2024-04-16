import pandas as pd

df = pd.read_csv("data (1).csv")
df.columns=["index", "link", "title", "comment_date", "comment","n_A", "label","made_by"] # df structure
# reformat comment_date
df["comment_date"] = df["comment_date"].apply(lambda x: "2021-01-01" if "nan" == str(x).lower() else x[:x.find("日")].replace("年", "-").replace("月", "-")) 
df['comment_date'] = pd.to_datetime(df['comment_date'], format='%Y-%m-%d')  
# remove unecessary columns
df.drop(["n_A", "made_by"], axis=1, inplace=True)
# add bank column: tag-like targeting title
textual_data = df.groupby("title", "comment")
textual_data.apply(lambda x: banks=[] banks.append("Citi") if "citi" in x else x banks.append("SCB") if "Standard Chartered" in x else x)



sort_bank = lambda x: "citi" if "citi" in x else "bank" if "bank" in x else "a" if "a" in x else "b" if "b" in x[::-1][:x[::-1].index(" ")] else "error"
df["bank"] = df["title"].apply(sort_bank)
# print(df.head(5))