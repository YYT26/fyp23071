from machine_learning import MachineLearning
import streamlit as st
import datetime
import pandas as pd
import plotly.express as px

st.title('Real-time Monitoring of Social Media Sentiment for Detecting Operational Incidents in Banking')

# current_time = datetime.datetime.now(pytz.timezone("Asia/Shanghai"))
# load
st.cache(allow_output_mutation=True)
def load():
    ML = pd.read_csv("processed_data.csv")
    return ML

with st.spinner("Please wait for data to load..."):
    df = load()
    df["comment_date"] = pd.to_datetime(df["comment_date"]).dt.strftime("%Y-%m-%d")
    date_range = sorted(df["comment_date"].unique().tolist()[::-1])


def reset():
    st.session_state.select_from = date_range[0]
    st.session_state.select_to = date_range[-1]

'To begin with the dashboard, head to the navigation bar on the left and select desired bank and date.'
with st.sidebar:
    st.subheader("1. Choose a bank:")
    bank_box = st.selectbox("Bank to be reviewed", ("HSBC - The Hongkong Shanghai Banking Corporation Limited", "SCB - Standarad Chartered Hong Kong", "HASE - Hang Seng Bank Limited", "Citi - Citibank (Hong Kong) Limited"))
    chosen_bank = bank_box[0:bank_box.find(" ")]
    st.subheader("2. Choose a period to preview: ")
    # dates = [date.strftime('%Y-%m-%d') for date in [start_date + datetime.timedelta(days=-i) for i in range(len(date_range))]]
    start_date = st.selectbox(label="From", options=date_range, placeholder="Please select a date...", index=2062, key="select_from")
    end_date = st.selectbox("To", [i for i in date_range[date_range.index(start_date):][::-1]], index=0, placeholder="Please select a date", key="select_to")
    reset_btn = st.button("Reset", on_click=reset)


period = date_range[date_range.index(start_date):date_range.index(end_date)+1]
st.divider()

st.info('You are looking at data of '+chosen_bank+' between '+start_date+" and "+end_date+".", icon="ℹ️")

with st.spinner("Loading data..."):
    # TODO #1 General: volume and senitment graph of data
    st.subheader("Executive Summary during the period")
    to_display = df[(df["comment_date"].isin(period)) & (df["bank"]==chosen_bank)]
    
    col1, col2 = st.columns(2)
    by_date = df[df["bank"]==chosen_bank].groupby('comment_date').size().reset_index(name='total_volume')
    fig = px.bar(by_date, x="comment_date", y="total_volume")
    fig.update_layout(
        title='Total Volume',
        xaxis_title='Dates',
        yaxis_title='Number of comments'
    )
    col1.plotly_chart(fig, use_container_width=True)
    # change df["sentiment"]
    col2.subheader("Average sentiment score: "+str(to_display["sentiment"].mean())[0:6])
    by_sentiment = to_display.groupby("bank").size().reset_index(name="portion")
    pie = px.pie(by_sentiment, values='portion', names='bank', title='Composition of sentiment score of each bank')
    col2.plotly_chart(pie, use_container_width=True)
    st.subheader("All comments:")
    st.dataframe(to_display)


# group shit by date, no need to loop

# df.groupby(["bank", pd.Grouper(key='date', freq='ME')]).[["sentiment"]].agg(np.mean).reset_index()
# reset_index --> keep data as data not index

