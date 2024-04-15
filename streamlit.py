from machine_learning import MachineLearning
import streamlit as st
import datetime

st.title('Real-time Monitoring of Social Media Sentiment for Detecting Operational Incidents in Banking')

# load
st.cache(allow_output_mutation=True)
def load():
    ML = MachineLearning("data (1).csv")
    return ML.preprocessing()
df=load()



current_time = datetime.now()

'Data updated at '+ current_time.year + "." + current_time.month + "." + current_time.day

'Auto-update is carried out at 01:00 every day.'

'Insights'



st.title('Filter by date')
period = st.selectbox("Please select the date: ", ("Today"))
'Date selected', period

# df.loc[df['comment_date']==period]


# group shit by date, no need to loop

# df.groupby(["bank", pd.Grouper(key='date', freq='ME')]).[["sentiment"]].agg(np.mean).reset_index()
# reset_index --> keep data as data not index

