import pandas as pd

df = pd.read_csv("data (1).csv")
df.columns=["index", "link", "title", "comment_date", "comment","n_A", "label","made_by"] # df structure

## remove unecessary columns
# df.drop(["n_A", "made_by"], axis=1, inplace=True)

# add bank column: tag-like targeting title
df_result = pd.read_csv("LIHKG_News_all_results.csv")
bank = []
for i in df.index:
    for j in df_result.index:
        if (df["comment_date"][i] == df_result["comment_date"][j]) and (df["comment"][i] == df_result["comment"][j]):
            bank.append(df_result["bank"][j])
            break
    bank.append("error")
            
print(len(df["bank"=="error"]))

## reformat comment_date
# df["comment_date"] = df["comment_date"].apply(lambda x: "2021-01-01" if "nan" == str(x).lower() else x[:x.find("日")].replace("年", "-").replace("月", "-")) 
# df['comment_date'] = pd.to_datetime(df['comment_date'], format='%Y-%m-%d')  

# comment_date missing --> take date afterwards

# textual_data = df.groupby("title", "comment")
# textual_data.apply(lambda x: banks=[] banks.append("Citi") if "citi" in x else x banks.append("SCB") if "Standard Chartered" in x else x)



