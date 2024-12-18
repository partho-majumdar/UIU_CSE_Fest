import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(layout="wide", page_title="Startup Analysis")

# Load the dataset
df = pd.read_csv("./startup_cleaned.csv")


def load_investor_details(investor):
    st.title(investor)

    # Load the recent 5 investments
    last_5_df = df[df["investors"].str.contains(investor, na=False)].head()[
        ["date", "startup", "vertical", "city", "round", "amount"]
    ]
    st.subheader("Most Recent Investments")
    st.dataframe(last_5_df)

    col1, col2 = st.columns(2)

    with col1:
        # Biggest investments
        big_series = (
            df[df["investors"].str.contains(investor, na=False)]
            .groupby("startup")["amount"]
            .sum()
            .sort_values(ascending=False)
        )
        st.subheader("Biggest Investments")
        st.bar_chart(big_series)

    with col2:
        # Sector investments
        vertical_series = (
            df[df["investors"].str.contains(investor, na=False)]
            .groupby("vertical")["amount"]
            .sum()
        )
        st.subheader("Sectors Invested In")
        st.write(vertical_series)  # Display data
        st.bar_chart(vertical_series)

    # Year-by-year investments
    st.subheader("Year-by-Year Investments")
    year_series = (
        df[df["investors"].str.contains(investor, na=False)]
        .groupby("year")["amount"]
        .sum()
    )
    st.line_chart(year_series)


def load_overall_analysis():
    st.title("Overall Analysis")

    # Total invested amount
    total = round(df["amount"].sum(), 2)

    # Maximum funding in a startup
    max_funding = (
        df.groupby("startup")["amount"].max().sort_values(ascending=False).iloc[0]
    )

    # Average funding
    avg_funding = round(df.groupby("startup")["amount"].sum().mean(), 2)

    # Total funded startups
    num_startups = df["startup"].nunique()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Funding", f"{total} cr")
    with col2:
        st.metric("Max Funding", f"{max_funding} cr")
    with col3:
        st.metric("Average Funding", f"{avg_funding} cr")
    with col4:
        st.metric("Number of Startups", num_startups)

    # Month-by-month graph
    st.header("Month-by-Month Analysis")
    selected_option = st.selectbox("Select Type", ["Total", "Count"])
    if selected_option == "Total":
        temp_df = df.groupby(["year", "month"])["amount"].sum().reset_index()
    else:
        temp_df = df.groupby(["year", "month"])["amount"].count().reset_index()

    temp_df["x_axis"] = temp_df["month"].astype(str) + "-" + temp_df["year"].astype(str)
    st.line_chart(temp_df.set_index("x_axis")["amount"])


# Sidebar options
st.sidebar.title("Startup Funding Analysis")
option = st.sidebar.selectbox(
    "Select an Option", ["Overall Analysis", "Startup", "Investor"]
)

if option == "Overall Analysis":
    load_overall_analysis()

elif option == "Startup":
    selected_startup = st.sidebar.selectbox(
        "Select Startup", sorted(df["startup"].unique())
    )
    btn1 = st.sidebar.button("Find Startup Details")
    if btn1:
        st.title(f"Analysis for {selected_startup}")

elif option == "Investor":
    selected_investor = st.sidebar.selectbox(
        "Select Investor", sorted(set(df["investors"].str.split(",").sum()))
    )
    btn2 = st.sidebar.button("Find Investor Details")
    if btn2:
        load_investor_details(selected_investor)
