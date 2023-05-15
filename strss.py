import pandas as pd
import streamlit as st
import requests
from datetime import datetime
import plotly.express as px

def get_info(): 

    df = pd.read_csv("C:/Users/arara/Documents/My_Progs/titanic/train.csv")

    print(df)

    url = "https://api.coincap.io/v2/assets"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    otvet = response.json()

    token_list = []
    for i in otvet["data"]:
        token_list.append(i["id"])
    print(token_list)

    st.title("Криптовалюты")

    curr = st.sidebar.selectbox("Select an asset", token_list)

    dtf = st.text_input("Date from")

    dtt = st.text_input("Date to")

    utc_time_dtf = datetime.strptime(dtf+"T00:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
    epoch_time_dtf = (utc_time_dtf - datetime(1970, 1, 1)).total_seconds() * 1000

    utc_time_dtt = datetime.strptime(dtt+"T00:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
    epoch_time_dtt = (utc_time_dtt - datetime(1970, 1, 1)).total_seconds() * 1000

    return curr, epoch_time_dtf, epoch_time_dtt

curr, epoch_time_dtf, epoch_time_dtt = get_info()

def get_plot(curr, epoch_time_dtf, epoch_time_dtt):

    url2 = "https://api.coincap.io/v2/assets/" + str(curr) + "/history?interval=d1&start=" + str(epoch_time_dtf) + "&end=" + str(epoch_time_dtt)

    payload2 = {}
    headers2  = {}

    response = requests.request("GET", url2, headers=headers2, data=payload2)

    otvet = response.json()

    df = pd.DataFrame.from_dict(otvet["data"])

    df['priceUsd'] = df['priceUsd'].astype(float).round(2)

    df["time"] = pd.cut(df["time"],10)

    df = df.groupby(["time"], as_index=False).agg(price=("priceUsd", "mean"))

    df["time"] = range(1,11)

    barr = px.bar(df, x = "time", y = "price")

    st.plotly_chart(barr, use_container_width=True)

get_plot(curr, epoch_time_dtf, epoch_time_dtt)