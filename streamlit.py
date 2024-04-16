from machine_learning import MachineLearning
import streamlit as st
import datetime
import pytz

st.title('Real-time Monitoring of Social Media Sentiment for Detecting Operational Incidents in Banking')

current_time = datetime.datetime.now(pytz.timezone("Asia/Shanghai"))

'To begin with the dashboard, head to the navigation bar on the left and select desired bank and date.'
with st.sidebar:
    st.subheader("1. Choose a bank:")
    bank = st.selectbox("Bank to be reviewed", ("HSBC - The Hongkong Shanghai Banking Corporation Limited", "SCB - Standarad Chartered Hong Kong", "HASE - Hang Seng Bank Limited", "Citi - Citibank (Hong Kong) Limited"))
    st.subheader("2. Choose a date to preview: ")
    start_time = pytz.timezone('Asia/Shanghai').localize(datetime.datetime(2021, 1, 1))
    dates = [current_time + datetime.timedelta(days=-i) for i in range((current_time - start_time).days + 1)]
    Dates = [date.strftime('%Y-%m-%d') for date in dates]
    period = st.selectbox("Please select the date: ", Dates)

st.divider()
st.info('You are looking at data of '+bank[0:bank.find(" ")]+' at '+period+".", icon="ℹ️")

# load
st.cache(allow_output_mutation=True)
def load():
    ML = MachineLearning("data (1).csv")
    return ML.preprocessing()

with st.spinner("Loading data..."):
    df=load()
    # fix data format
    # display = df.loc[df['comment_date']==period && df["bank"]==bank]
    st.dataframe(df)




# group shit by date, no need to loop

# df.groupby(["bank", pd.Grouper(key='date', freq='ME')]).[["sentiment"]].agg(np.mean).reset_index()
# reset_index --> keep data as data not index

