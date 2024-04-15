from machine_learning import MachineLearning
import streamlit as st
import datetime
import pytz

st.title('Real-time Monitoring of Social Media Sentiment for Detecting Operational Incidents in Banking')

# # load
# st.cache(allow_output_mutation=True)
# def load():
#     ML = MachineLearning("data (1).csv")
#     return ML.preprocessing()
# df=load()



current_time = datetime.datetime.now(pytz.timezone("Asia/Shanghai"))

'Data updated at ' + str(current_time.strftime("%Y/%m/%d")) + "."

'[To be removed] Auto-update is carried out at 01:00 every day.'

st.title('Insights')
st.button("HSBC", key="hsbc")
st.button("Standard Chartered Hong Kong", key="scb")
st.button("Bank of China (HK)", key="bochk")
st.button("Citibank (Hong Kong)", key="citi")


st.divider()

st.title('Filter by date')
start_time = pytz.timezone('Asia/Shanghai').localize(datetime.datetime(2021, 1, 1))
dates = [current_time + datetime.timedelta(days=-i) for i in range((current_time - start_time).days + 1)]
dates_f = [date.strftime('%Y-%m-%d') for date in dates]
period = st.selectbox("Please select the date: ", dates_f)
'Date selected', period + "."

# df.loc[df['comment_date']==period]

# st.dataframe(df)


# group shit by date, no need to loop

# df.groupby(["bank", pd.Grouper(key='date', freq='ME')]).[["sentiment"]].agg(np.mean).reset_index()
# reset_index --> keep data as data not index

