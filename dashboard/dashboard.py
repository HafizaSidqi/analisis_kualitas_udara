# import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# membuat fungsi untuk menyiapkan monthly_df
def create_monthly_df(main_df, polutan, input_station):
    monthly_df = pd.DataFrame()
    if len(input_station) == 0:
        return monthly_df
    for i in input_station:
        df = main_df[main_df['station']==i].resample(rule='M',on='datetime').agg({
            "station": "unique",
            polutan: "mean"
        })
        monthly_df = pd.concat([monthly_df, df], ignore_index=False)
    monthly_df.index = monthly_df.index.strftime('%Y-%m')
    monthly_df = monthly_df.reset_index()
    monthly_df = monthly_df.explode("station", ignore_index=False)
    return monthly_df

# membuat prosedur untuk membuat linechart
def create_line_chart(month_df, polutan,input_station):
    fig, ax = plt.subplots(figsize=(20,5))
    for i in input_station:
        ax.plot(month_df['datetime'].loc[month_df['station']==i],
                month_df[polutan].loc[month_df['station']==i],
                label=i, marker='o', linewidth=2)
    ax.set_title("Number of "+polutan, loc="center", fontsize=20)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=15, rotation=45)
    ax.tick_params(axis='y', labelsize=15)
    ax.legend(bbox_to_anchor=(1,1))
    st.pyplot(fig)

# membuat prosedure untuk membuat barchart
def create_best_worst_bar_chart(month_df, polutan):
    lowest_5 = month_df.sort_values(by=polutan, ascending=True).head(5)
    highest_5 = month_df.sort_values(by=polutan, ascending=False).head(5)

    lowest_5["datetime_station"]= lowest_5['datetime']+' '+lowest_5['station']
    highest_5["datetime_station"]= highest_5['datetime']+' '+highest_5['station']
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

    sns.barplot(y="datetime_station", x=polutan, data=highest_5,
                palette=colors, hue='datetime_station', legend=False,ax=ax[0])
    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("Highest "+polutan, loc="center", fontsize="15")
    ax[0].tick_params(axis='y', labelsize=12)
    ax[0].annotate(round(highest_5[polutan].iloc[0], 2),
                   xy=(highest_5[polutan].iloc[0], highest_5["datetime_station"].iloc[0]),
                   fontsize=15)
    
    sns.barplot(y="datetime_station", x=polutan, data=lowest_5,
                palette=colors, hue="datetime_station", legend=False, ax=ax[1])
    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    if polutan != "TEMP":
        ax[1].invert_xaxis()
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].set_title("Lowest "+polutan, loc="center", fontsize="15")
    ax[1].tick_params(axis='y', labelsize=12)
    ax[1].annotate(round(lowest_5[polutan].iloc[0], 2),
                   xy=(lowest_5[polutan].iloc[0], lowest_5["datetime_station"].iloc[0]),
                   fontsize=15)
    
    plt.suptitle("Highest and Lowest "+polutan, fontsize=20)
    st.pyplot(fig)

# menampilkan grafik
def show_graph(polutan):
    month_df = create_monthly_df(main_df, polutan, input_station)
    if len(month_df) != 0:
        create_line_chart(month_df, polutan, input_station)
        create_best_worst_bar_chart(month_df, polutan)

# load data
all_df = pd.read_pickle("dashboard/all_df.pkl")

# Berikutnya adalah menambahkan filter pada dashboard dengan menggunakan widget date input pada bagian sidebar
min_date = all_df["datetime"].min()
max_date = all_df["datetime"].max()

with st.sidebar:
    # menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")

    # menambahkan start_date dan end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# start_date dan end_date di atas akan digunakan untuk memfilter all_df dan disimpan pada main_df
main_df = all_df[(all_df["datetime"] >= str(start_date))&(all_df["datetime"] <= str(end_date))]

# melengkapi dashboard dengan visualisasi data
st.header('Air Quality Dashboard :sparkles:')

# mengambil input stasiun yang ingin ditampilkan
input_station = st.multiselect(
    label= "Which station do you want to see?",
    options=all_df["station"].unique()
)

# mengambil parameter polutan yang ingin ditampilkan
col1, col2 = st.columns(2)
with col1:
    PM25 = st.checkbox("PM2.5")
    PM10 = st.checkbox("PM10")
    SO2 = st.checkbox("SO2")
    NO2 = st.checkbox("NO2")
with col2:
    CO = st.checkbox("CO")
    O3 = st.checkbox("O3")
    TEMP = st.checkbox("TEMP")
    RAIN = st.checkbox("RAIN")

# Grafik
if PM25:
    show_graph("PM2.5")
if PM10:
    show_graph("PM10")
if SO2:
    show_graph("SO2")
if NO2:
    show_graph("NO2")
if CO:
    show_graph("CO")
if O3:
    show_graph("O3")
if TEMP:
    show_graph("TEMP")
if RAIN:
    show_graph("RAIN")
