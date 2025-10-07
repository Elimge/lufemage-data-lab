# app.py 

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Lufemage Data Lab - Sales Analysis",
    page_icon="📊",
    layout="wide",
)

# --- FUNCTION TO LOAD DATA (with caching) ---
# Using st.cache_data to cache the data loading function
@st.cache_data
def load_data():
    df = pd.read_csv("data/raw_sales_data.csv")
    df["fecha_compra"] = pd.to_datetime(df["fecha_compra"])
    df["hora_dia"] = df["fecha_compra"].dt.hour
    df["dia_semana"] = df["fecha_compra"].dt.day_name()
    
    return df

df = load_data()

# --- TITLE AND DESCRIPTION ---
st.title("📊 Lufemage Data Lab - Sales Analysis")
st.write("An interactive dashboard to explore sales data from Lufemage Data Labs.")

# --- SIDEBAR FOR FILTERS ---
st.sidebar.header("Filter Data")

# City filter
selected_cities = st.sidebar.multiselect(
    "Select Cities:",
    options=df["ciudad"].unique(),
    default=df["ciudad"].unique() # Select all by default
)

# Product category filter (selectbox)
selected_category = st.sidebar.selectbox(
    "Select Product Category:",
    options=['All'] + list(df['categoria_producto'].unique())
)

# --- DATAFRAME FILTERING ---
df_filtered = df[df["ciudad"].isin(selected_cities)]

if selected_category != "All":
    df_filtered = df_filtered[df_filtered["categoria_producto"] == selected_category]

# --- KPIS ---
total_sales = df_filtered["monto"].sum()
average_ticket = df_filtered["monto"].mean()
total_transactions = df_filtered.shape[0]

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Sales", f"${total_sales:,.2f}")
with col2:
    st.metric("Average Ticket Size", f"${average_ticket:,.2f}")
with col3:
    st.metric("Total Transactions", f"{total_transactions}")

st.markdown("---")

# --- VISUALIZATIONS ---
col_left, col_right = st.columns(2)

with col_left:
    # Sales by Hour of Day
    st.subheader("Sales by Hour of Day")
    sales_by_hour = df_filtered.groupby("hora_dia")["monto"].sum()
    fig1, ax1 = plt.subplots()
    sns.lineplot(x=sales_by_hour.index, y=sales_by_hour.values, marker="o", ax=ax1)
    ax1.set_xlabel("Hour of Day")
    ax1.set_ylabel("Total Sales")
    st.pyplot(fig1)

with col_right:
    # Sales by Day of Week
    st.subheader("Sales by Day of Week")
    sales_by_day = df_filtered.groupby("dia_semana")["monto"].sum().reindex(
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    )
    fig2, ax2 = plt.subplots()
    sns.barplot(x=sales_by_day.index, y=sales_by_day.values, ax=ax2)
    ax2.set_xlabel("Day of Week")
    ax2.set_ylabel("Total Sales")
    plt.xticks(rotation=45)
    st.pyplot(fig2)

# Show the filtered dataframe
st.markdown("---")
st.subheader("Filtered Sales Data")
st.dataframe(df_filtered)

