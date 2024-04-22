import streamlit as st
import pandas as pd
import plotly.express as px

st.title('Real-time Monitoring of Social Media Sentiment for Detecting Operational Incidents in Banking')

# load
st.cache(allow_output_mutation=True)
def load():
    ML = pd.read_csv("processed_data.csv")
    return ML


with st.spinner("Please wait for data to load..."):
    df = load()
    df["comment_date"] = pd.to_datetime(df["comment_date"]).dt.strftime("%Y-%m-%d")
    date_range = sorted(df["comment_date"].unique().tolist()[::-1])
    bank_dic = {"HSBC": "HSBC - The Hongkong Shanghai Banking Corporation Limited", "SCB": "SCB - Standard Chartered Hong Kong", "HASE": "HASE - Hang Seng Bank Limited", "Citi": "Citi - Citibank (Hong Kong) Limited"}


'To begin with the dashboard, head to the navigation bar on the left and select desired bank and date.'
st.divider()

with st.sidebar:
    # choose date
    st.subheader("1. Choose a period to preview: ")
    start_date = st.selectbox(label="From", options=date_range, placeholder="Please select a date...", index=2062, key="select_from")
    end_date = st.selectbox("To", [i for i in date_range[date_range.index(start_date):][::-1]], index=0, placeholder="Please select a date", key="select_to")
    period = date_range[date_range.index(st.session_state.select_from):date_range.index(st.session_state.select_to)+1]
    
    # choose bank
    st.subheader("2. Choose a bank:")
    bank_keys = df[df["comment_date"].isin(period)]["bank"].unique().tolist()
    print(bank_keys)
    bank_list = [bank_dic.get(i, "error") for i in bank_keys]
    bank_box = st.selectbox("Bank to be reviewed", bank_list, index=0, placeholder="Open the dropdown menu for available", key="select_bank")
    chosen_bank = bank_box[0:bank_box.find(" ")]


with st.spinner("Please wait for data to load..."):
    # Total volume
    by_date = df[df["bank"]==chosen_bank].groupby('comment_date').size().reset_index(name='total_volume')
    fig = px.bar(by_date, x="comment_date", y="total_volume")
    fig.update_layout(
        title='Total Volume of all available dates of '+bank_box+' - Feel free to interact with below graph',
        xaxis_title='Dates',
        yaxis_title='Number of comments'
    )
    st.plotly_chart(fig, use_container_width=True)


    st.header("Executive Summary during the period")
    to_display = df[(df["comment_date"].isin(period)) & (df["bank"]==chosen_bank)]

    st.info('You are looking at data of '+chosen_bank+' between '+start_date+" and "+end_date+".", icon="ℹ️")
    st.subheader("Average sentiment score: "+str(to_display["sentiment"].mean())[0:6])

    # Pie chart
    by_sentiment = df[df["comment_date"].isin(period)].bank.to_list()
    bank_count = {i: 0 for i in list(bank_dic.keys())}
    for i in by_sentiment:
        if "[" not in i:
            bank_count[i] += 1
        else:
            for j in eval(i):
                bank_count[j]+=1 
    bank_count = pd.DataFrame(list(bank_count.items()), columns=['Bank', 'Number'])
    pie = px.pie(bank_count, values='Number', names='Bank', title='Number of comments of all banks during the period')
    st.plotly_chart(pie, use_container_width=True)

    # Display all comments during the period of the bank
    st.subheader("All comments:")
    st.dataframe(to_display)

