import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="startup_analysis")  # this spread space

df = pd.read_csv("./startup_cleaned.csv")


def load_investor_details(investor):
    st.title(investor)

    # load the recent 5 investment
    last_5_df = df[df["investors"].str.contains(investor)].head()[
        ["date", "startup", "vertical", "city", "round", "amount"]
    ]
    st.subheader("Most recent investment")
    st.dataframe(last_5_df)

    col1, col2 = st.columns(2)
    with col1:
        # biggest investment
        big_series = (
            df[df["investors"].str.contains(investor)]
            .groupby("startup")["amount"]
            .sum()
            .sort_values(ascending=False)
        )
        st.subheader("Biggest investments")
        # st.dataframe(big_df)
        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)
        st.pyplot(fig)

    with col2:
        vertical_series = (
            df[df["investors"].str.contains(investor)]
            .groupby("vertical")["amount"]
            .sum()
        )
        st.subheader("Sector invested in")
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series, labels=vertical_series.index, autopct="%0.01f%%")
        st.pyplot(fig1)

    # year by year investments
    st.subheader("Year by year investments: ")
    # df['year'] = df['date'].dt.year
    year_series = (
        df[df["investors"].str.contains(investor)].groupby("year")["amount"].sum()
    )
    fig2, ax2 = plt.subplots()
    ax2.plot(year_series.index, year_series.values)
    st.pyplot(fig2)


def load_overall_analysis():
    st.title("Overall analysis")

    # total invested amount
    total = round(df["amount"].sum())

    # max amount in startup
    max_funding = (
        df.groupby("startup")["amount"]
        .max()
        .sort_values(ascending=False)
        .head(1)
        .values[0]
    )

    # avg funding
    avg_funding = round(df.groupby("startup")["amount"].sum().mean(), 2)

    # total funded startup
    num_startups = df["startup"].nunique()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total", str(total) + " cr")
    with col2:
        st.metric("Max funding", str(max_funding) + " cr")
    with col3:
        st.metric("Avg", str(avg_funding) + " cr")
    with col4:
        st.metric("Number of startups", str(num_startups))

    # month on month graph
    st.header("Month by Month Graph")
    selected_option = st.selectbox("Select type", ["Total", "count"])
    if selected_option == "Total":
        temp_df = df.groupby(["year", "month"])["amount"].sum().reset_index()
    else:
        temp_df = df.groupby(["year", "month"])["amount"].count().reset_index()

    temp_df["x_axis"] = (
        temp_df["month"].astype("str") + "-" + temp_df["year"].astype("str")
    )
    fig3, ax3 = plt.subplots()
    ax3.plot(temp_df["x_axis"], temp_df["amount"])
    st.pyplot(fig3)


st.sidebar.title("Startup Funding Analysis")
option = st.sidebar.selectbox(
    "Select one of them", ["Overall Analysis", "Startup", "Investor"]
)

if option == "Overall Analysis":
    # st.title("Overall analysis")
    # btn0 = st.sidebar.button("Show overall analysis")
    # if btn0:
    load_overall_analysis()


elif option == "Startup":
    st.sidebar.selectbox("Select startup", sorted(df["startup"].unique().tolist()))
    btn1 = st.sidebar.button("Find Startup Details")
    st.title("Startup analysis")

elif option == "Investor":
    selected_investor = st.sidebar.selectbox(
        "Select investor", sorted(set(df["investors"].str.split(",").sum()))
    )
    btn2 = st.sidebar.button("Find Investor Details")
    if btn2:
        load_investor_details(selected_investor)

    # st.title("Investor analysis")
