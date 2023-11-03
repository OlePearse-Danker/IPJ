import pandas as pd
import csv
import matplotlib.pyplot as plt
import matplotlib.style as style
import datetime
import time
import streamlit as st
from matplotlib.animation import FuncAnimation
import numpy as np
import plotly.express as px



# Apply dark background style
style.use('dark_background')

st.title("WATT-Meister-Consulting Calculator")
st.divider()
st.subheader('Energy production and consumption')
st.write('For the following plots, we collected the electricity market data of Germany for the years 2020, 2021, and 2022 and analyzed the production and consumption. In the first plot, you can see the production and consumption for any specific day in the period from 2020 to 2022.')

start_date = datetime.date(2020, 1, 1)
end_date = datetime.date(2022, 12, 31)
default_date = datetime.date(2020, 1, 1)
st.write("##")
input_date = st.date_input("Select a Date",value = default_date, min_value=start_date, max_value=end_date)

def parse_datetime(date_str, time_str):
    return datetime.datetime.strptime(f"{date_str} {time_str}", "%d.%m.%Y %H:%M")

startzeit = time.time()

csv_datei1 = 'Realisierte_Erzeugung_202001010000_202212312359_Viertelstunde.csv'
csv_datei2 = 'Realisierter_Stromverbrauch_202001010000_202212312359_Viertelstunde.csv'


energie_daten = []
energie_daten2 = []
production = []
consumption = []

with open(csv_datei1, 'r') as file:
    csv_reader = csv.reader(file, delimiter=';')
    next(csv_reader)
    for row in csv_reader:
        datum = row[0]
        anfang = row[1]
        ende = row[2]
        biomasse = float(row[3].replace('.', '').replace(',', '.'))
        wasserkraft = float(row[4].replace('.', '').replace(',', '.'))
        wind_offshore = float(row[5].replace('.', '').replace(',', '.'))
        wind_onshore = float(row[6].replace('.', '').replace(',', '.'))
        photovoltaik = float(row[7].replace('.', '').replace(',', '.'))
        try:
            sonstige_erneuerbare = float(row[8].replace('.', '').replace(',', '.')) 
        except ValueError:
            sonstige_erneuerbare = 0.0
        kernenergie = float(row[9].replace('.', '').replace(',', '.'))
        braunkohle = float(row[10].replace('.', '').replace(',', '.'))
        steinkohle = float(row[11].replace('.', '').replace(',', '.'))
        erdgas = float(row[12].replace('.', '').replace(',', '.'))
        pumpspeicher = float(row[13].replace('.', '').replace(',', '.'))
        sonstige_konventionelle = float(row[14].replace('.', '').replace(',', '.'))

        datensatz = {
            'Datum': datum,
            'Anfang': anfang,
            'Ende': ende,
            'Biomasse [MWh]': biomasse,
            'Wasserkraft [MWh]': wasserkraft,
            'Wind Offshore [MWh]': wind_offshore,
            'Wind Onshore [MWh]': wind_onshore,
            'Photovoltaik [MWh]': photovoltaik,
            'Sonstige Erneuerbare [MWh]': sonstige_erneuerbare,
            'Kernenergie [MWh]': kernenergie,
            'Braunkohle [MWh]': braunkohle,
            'Steinkohle [MWh]': steinkohle,
            'Erdgas [MWh]': erdgas,
            'Pumpspeicher [MWh]': pumpspeicher,
            'Sonstige Konventionelle [MWh]': sonstige_konventionelle
        }
        energie_daten.append(datensatz)


# reading in the data as a dataframe



with open(csv_datei2, 'r') as file:
    csv_reader = csv.reader(file, delimiter=';')
    next(csv_reader)
    for row in csv_reader:
        datum = row[0]
        anfang = row[1]
        gesamt = float(row[3].replace('.', '').replace(',', '.'))

        datensatz1 = {
            'Datum': datum,
            'Anfang': anfang,
            'Gesamt (Netzlast) [MWh]': gesamt,
        }
        energie_daten2.extend([datensatz1])



production = [datensatz['Biomasse [MWh]'] + datensatz['Wasserkraft [MWh]'] + datensatz['Wind Offshore [MWh]'] + datensatz['Wind Onshore [MWh]'] + datensatz['Photovoltaik [MWh]'] + datensatz['Sonstige Erneuerbare [MWh]'] for datensatz in energie_daten]

consumption = [datensatz1['Gesamt (Netzlast) [MWh]'] for datensatz1 in energie_daten2]
    

selected_date = input_date
filtered_data = [datensatz for datensatz in energie_daten if parse_datetime(datensatz['Datum'], datensatz['Anfang']).date() == selected_date]
filtered_data2 = [datensatz1 for datensatz1 in energie_daten2 if parse_datetime(datensatz1['Datum'], datensatz1['Anfang']).date() == selected_date]


hours = [parse_datetime(datensatz['Datum'], datensatz['Anfang']).hour + parse_datetime(datensatz['Datum'], datensatz['Anfang']).minute / 60 for datensatz in filtered_data]
production_day = [datensatz['Biomasse [MWh]'] + datensatz['Wasserkraft [MWh]'] + datensatz['Wind Offshore [MWh]'] + datensatz['Wind Onshore [MWh]'] + datensatz['Photovoltaik [MWh]'] + datensatz['Sonstige Erneuerbare [MWh]'] for datensatz in filtered_data]
consumption_day = [datensatz1['Gesamt (Netzlast) [MWh]'] for datensatz1 in filtered_data2]

def range1(array1, array2):
    if len(array1) != len(array2):
        raise ValueError("Arrays must be the same length")
    
    count10 = 0
    count20 = 0
    count30 =0
    count40 = 0
    count50 = 0
    count60 = 0
    count70 = 0
    count80 = 0
    count90 = 0
    count100 = 0

    for val1, val2 in zip(array1, array2):
        if 0.1 <= val1 / val2 < 0.2:
            count10 += 1
        if 0.2 <= val1 / val2 < 0.3:
            count20 +=1
        if 0.3 <= val1 / val2 < 0.4:
            count30 +=1
        if 0.4 <= val1 / val2 < 0.5:
            count40 +=1
        if 0.5 <= val1 / val2 < 0.6:
            count50 +=1
        if 0.6 <= val1 / val2 < 0.7:
            count60 +=1
        if 0.7 <= val1 / val2 < 0.8:
            count70 +=1
        if 0.8 <= val1 / val2 < 0.9:
            count80 +=1
        if 0.9 <= val1 / val2 < 1:
            count90 +=1
        if  val1 / val2  == 1:
            count100+=1

    return [count10, count20, count30, count40, count50, count60, count70, count80, count90, count100]

counts =[]
counts = range1(production, consumption)
print(counts)


def animate(i):

    ax1 = plt.subplots(figsize=(12, 6))

    ax1.plot(hours, consumption_day, label='Consumption')
    ax1.plot(hours, production_day, label='Production (renewable energy)', linewidth=2.5)
 
    ax1.set_xlabel('Time [Hour]')
    ax1.set_ylabel('Power (MWh)')




if input_date:
    selected_date = datetime.datetime.strptime(str(input_date), "%Y-%m-%d").date()

    # Create the figure and axes objects for the first plot
    fig1, ax1 = plt.subplots(figsize=(12, 6))

    ax1.plot(hours, consumption_day, label='Consumption')
    ax1.plot(hours, production_day, label='Production (renewable energy)', linewidth=2.5)
 
    ax1.set_xlabel('Time [Hour]')
    ax1.set_ylabel('Power (MWh)')
    ax1.set_title(f'Energy production and consumption for {selected_date.strftime("%d.%m.%Y")}')
    ax1.fill_between(hours, consumption_day)
    ax1.fill_between(hours, production_day)
    ax1.legend()


    # plt.tight_layout()
    ax1.grid(True)
    ax1.set_xticks(range(0, 24))
    

    # Create the figure and axes objects for the second plot
fig2, ax2 = plt.subplots(figsize=(6, 4))

    # Set the x-tick positions and labels
x_ticks = range(len(counts))
x_labels = ['10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%']
ax2.set_xticks(x_ticks)
ax2.set_xticklabels(x_labels)

ax2.bar(x_ticks, counts)
ax2.set_title('Anzahl der Viertelstunden mit 10-100 % EE-Anteil')



# ... Remaining code omitted for brevity ...

if input_date:


    st.pyplot(fig1)


    st.write("##")
    st.write("##")
    st.subheader('Amount of quarter hours with Renewable Energy in Percent')
    st.markdown("---")
    st.pyplot(fig2)



# reading in data as a dataframe
df = pd.read_csv(csv_datei1, delimiter=";")
df['Datum'] = pd.to_datetime(df['Datum'], format='%d.%m.%Y')
df['Anfang'] = pd.to_datetime(df['Anfang'], format='%H:%M')
df['Ende'] = pd.to_datetime(df['Ende'], format='%H:%M')


df['Wasserkraft [MWh] Originalauflösungen'] = df['Wasserkraft [MWh] Originalauflösungen'].str.replace(".", "").str.replace(",", ".").astype(float)
df['Biomasse [MWh] Originalauflösungen'] = df['Biomasse [MWh] Originalauflösungen'].str.replace(".", "").str.replace(",", ".").astype(float)
df['Wind Offshore [MWh] Originalauflösungen'] = df['Wind Offshore [MWh] Originalauflösungen'].str.replace(".", "").str.replace(",", ".").astype(float)
df['Wind Onshore [MWh] Originalauflösungen'] = df['Wind Onshore [MWh] Originalauflösungen'].str.replace(".", "").str.replace(",", ".").astype(float)
df['Photovoltaik [MWh] Originalauflösungen'] = df['Photovoltaik [MWh] Originalauflösungen'].str.replace(".", "").str.replace(",", ".").astype(float)

column_name = 'Sonstige Erneuerbare [MWh] Originalauflösungen'

for idx, value in enumerate(df[column_name]):
    try:
        df.at[idx, column_name] = float(value.replace(".", "").replace(",", "."))
    except (ValueError, AttributeError):
        df.at[idx, column_name] = 0


df['Kernenergie [MWh] Originalauflösungen'] = df['Kernenergie [MWh] Originalauflösungen'].str.replace(".", "").str.replace(",", ".").astype(float)
df['Braunkohle [MWh] Originalauflösungen'] = df['Braunkohle [MWh] Originalauflösungen'].str.replace(".", "").str.replace(",", ".").astype(float)
df['Steinkohle [MWh] Originalauflösungen'] = df['Steinkohle [MWh] Originalauflösungen'].str.replace(".", "").str.replace(",", ".").astype(float)
df['Erdgas [MWh] Originalauflösungen'] = df['Erdgas [MWh] Originalauflösungen'].str.replace(".", "").str.replace(",", ".").astype(float)
df['Pumpspeicher [MWh] Originalauflösungen'] = df['Pumpspeicher [MWh] Originalauflösungen'].str.replace(".", "").str.replace(",", ".").astype(float)
df['Sonstige Konventionelle [MWh] Originalauflösungen'] = df['Sonstige Konventionelle [MWh] Originalauflösungen'].str.replace(".", "").str.replace(",", ".").astype(float)


# printing the day of the week
# print(df['Datum'].dt.day_name())

# data for 2020 (via filtering)
filt_20 = ((df['Datum'] >= pd.to_datetime('01.01.2020')) & (df['Datum'] < pd.to_datetime('01.01.2021')))
# print(df.loc[filt_20])

# setting the date as an index 
df.set_index('Datum', inplace=True)

bio_mean = round(df['Biomasse [MWh] Originalauflösungen'].mean(), 2)
water_mean = round(df['Wasserkraft [MWh] Originalauflösungen'].mean(), 2)
windoff_mean = round(df['Wind Offshore [MWh] Originalauflösungen'].mean(), 2)
windon_mean = round(df['Wind Onshore [MWh] Originalauflösungen'].mean(), 2)
pv_mean = round(df['Photovoltaik [MWh] Originalauflösungen'].mean(), 2)
other_re_mean = round(df['Sonstige Erneuerbare [MWh] Originalauflösungen'].mean(), 2)
nuclear_mean = round(df['Kernenergie [MWh] Originalauflösungen'].mean(), 2)
bc_mean = round(df['Braunkohle [MWh] Originalauflösungen'].mean(), 2)
sc_mean = round(df['Steinkohle [MWh] Originalauflösungen'].mean(), 2)
gas_mean = round(df['Erdgas [MWh] Originalauflösungen'].mean(), 2)
ps_mean = round(df['Pumpspeicher [MWh] Originalauflösungen'].mean(), 2)
other_conv = round(df['Sonstige Konventionelle [MWh] Originalauflösungen'].mean(), 2)




st.subheader("Daily Average Production")
st.write("In the following you can see the daily average over the last three years for the specific production kind")

col1, col2, col3 = st.columns(3)


with col1:
    st.metric(label="Biomass [MWh]", value=bio_mean)
    st.metric(label="Waterpower [MWh]", value=water_mean)
    st.metric(label="Wind Offshore [MWh]", value=windoff_mean)
    st.metric(label="Wind Onshore [MWh]", value=windon_mean)

with col2:
    st.metric(label="Photovoltaic [MWh]", value=pv_mean)
    st.metric(label="Other Renewable [MWh]", value=other_re_mean)
    st.metric(label="Nuclear [MWh]", value=nuclear_mean)
    st.metric(label="Brown Coal [MWh]", value=bc_mean)

with col3:
    st.metric(label="Hard Coal [MWh]", value=sc_mean)
    st.metric(label="Gas [MWh]", value=gas_mean)
    st.metric(label="Pump storage [MWh]", value=ps_mean)
    st.metric(label="Other Conventional [MWh]", value=other_conv)


# df.reset_index(inplace=True)

ree_production_sum = ['Wasserkraft [MWh] Originalauflösungen', 'Biomasse [MWh] Originalauflösungen',
                  'Wind Offshore [MWh] Originalauflösungen', 'Wind Onshore [MWh] Originalauflösungen',
                  'Photovoltaik [MWh] Originalauflösungen', 'Sonstige Erneuerbare [MWh] Originalauflösungen']
df['Renewable Energy Sum [MWh]'] = df[ree_production_sum].sum(axis=1)
# testing bar charts


st.subheader('Production of Renewable Energy')
year_options = [2020, 2021, 2022]
year = st.selectbox('Which year would you like to see?', year_options)

if year == 2020:
    start_date = '2020-01-01'
    end_date = '2020-12-31'
    filtered_df = df[(df.index >= start_date) & (df.index <= end_date)]
    total_production = filtered_df['Renewable Energy Sum [MWh]'].sum()

if year == 2021:
    start_date = '2021-01-01'
    end_date = '2021-12-31'
    filtered_df = df[(df.index >= start_date) & (df.index <= end_date)]
    total_production = filtered_df['Renewable Energy Sum [MWh]'].sum()

if year == 2022:
    start_date = '2022-01-01'
    end_date = '2022-12-31'
    filtered_df = df[(df.index >= start_date) & (df.index <= end_date)]
    total_production = filtered_df['Renewable Energy Sum [MWh]'].sum()

fig = px.bar(filtered_df, x=filtered_df.index, y='Renewable Energy Sum [MWh]')
fig.update_layout(width=800)
st.write(fig)
st.metric(label='Renwable Energy production for ' + str(year) + ' [MWh]', value=total_production)



endzeit = time.time()
dauer = endzeit - startzeit
st.write(f"Startzeit: {startzeit}")
st.write(f"Endzeit: {endzeit}")
st.write(f"Dauer des Programms: {dauer} Sekunden")