from machine_learning import MachineLearning
import streamlit as st
import datetime
import pytz
import pandas as pd
import plotly.figure_factory as ff

st.title('Real-time Monitoring of Social Media Sentiment for Detecting Operational Incidents in Banking')

# current_time = datetime.datetime.now(pytz.timezone("Asia/Shanghai"))
# load
st.cache(allow_output_mutation=True)
def load():
    ML = pd.read_csv("processed_data.csv")
    return ML

with st.spinner("Please wait for data to load..."):
    df = load()
    date_range = df.comment_date # array
    start_date = df.comment_date[-1]
    end_date = df.comment_date[0]

'To begin with the dashboard, head to the navigation bar on the left and select desired bank and date.'
with st.sidebar:
    st.subheader("1. Choose a bank:")
    bank = st.selectbox("Bank to be reviewed", ("HSBC - The Hongkong Shanghai Banking Corporation Limited", "SCB - Standarad Chartered Hong Kong", "HASE - Hang Seng Bank Limited", "Citi - Citibank (Hong Kong) Limited"))
    st.subheader("2. Choose a period to preview: ")
    start_time = pytz.timezone('Asia/Shanghai').localize(datetime.datetime(2021, 1, 1))
    dates = [date.strftime('%Y-%m-%d') for date in [datetime.timedelta(days=-i) for i in date_range]]
    end_date = st.selectbox("To ", dates)
    start_date = st.selectbox("From", [i for i in dates[dates.find(end_date):]])
period = [date.strftime('%Y-%m-%d') for date in [start_date + datetime.timedelta(days=-i) for i in range(end_date - start_date)]]
st.divider()

st.info('You are looking at data of '+bank[0:bank.find(" ")]+' between '+start_date+" and "+end_date+".", icon="ℹ️")

# TODO #1 General: volume and senitment graph of data
"Executive Summary"
col1, col2 = st.columns(2)
volume = df["comment_date"].count()
fig = ff.create_distplot(volume)
col1.write("Total volume")
col1.plotly_graph(fig)
col2.write("Average sentiment score")
col2.subheader(df["sentiment"].mean())

# TODO #2 General: data sorted by date

with st.spinner("Loading data..."):
    by_date = df.groupby("comment_date", as_index=False)
    output = pd.concat([group for (day, group) in by_date if day in period])
    # display = df.loc[df['comment_date']==period && df["bank"]==bank]
    st.dataframe(df)

    volume = []

    sentiment = 1

    "Volume of the day:", volume
    "Sentiment score of the day: ", sentiment*100


# group shit by date, no need to loop

# df.groupby(["bank", pd.Grouper(key='date', freq='ME')]).[["sentiment"]].agg(np.mean).reset_index()
# reset_index --> keep data as data not index

