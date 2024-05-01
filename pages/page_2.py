import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import plotly.express as px
from streamlit_folium import folium_static
from streamlit_folium import st_folium

st.subheader("If you were to ask someone why they don't take climate change seriously, they may respond with, 'So the world gets a little warmer, so what?'.")
st.text("Unfortunately, climate change has a much larger impact on society than is believed. \nIf air pollutants cause the greenhouse effect, what do you think they do to \nhumans when breathed in?")
st.subheader("The three pollutants below are linked to cardiovascular and respiratory diseases in humans, acid rain, and vegetation damage.")
st.text("Nitrogen dioxide(NO2) is formed from the combustion of diesel engines, coal, and \nwaste plants.  It contributes to the formation of ground-level ozone(O3) and \nparticulate black carbon (PM2.5), the other two major air pollutants.")
airquality=pd.read_csv('https://raw.githubusercontent.com/mackenzieklein/CSVs-for-Final/main/world_air_quality.csv')
pollutant = st.selectbox(
    'Choose one of the air pollutants below.',
    ('NO2', 'O3', 'PM2.5'))
airquality['value'] = airquality['value'].str.replace('Jan-00', '0')
airquality['value']=airquality['value'].astype(float)

if pollutant=='NO2':
  airquality2=airquality.loc[airquality['pollutant']=='NO2',['country', 'value']]
  grouped1=airquality2.groupby(["country"], as_index=False)["value"].mean()
  fig1=plt.figure()
  ax1=fig1.add_subplot()
  ax1.plot(grouped1['country'], grouped1['value'])
  ax1.set_title("Average Level of Pollutant by Country (2023-2024)")
  ax1.set_xlabel('Country')
  ax1.set_ylabel('NO2 Concentration (micrograms per cubic meter)')
  plt.xticks(rotation=90)
  st.pyplot(fig1)
elif pollutant=='O3':
  airquality3=airquality.loc[airquality['pollutant']=='O3', ['country', 'value']]
  grouped2=airquality3.groupby(['country'], as_index=False)['value'].mean()
  fig2=plt.figure()
  ax2=fig2.add_subplot()
  ax2.plot(grouped2['country'], grouped2['value'])
  ax2.set_title("Average Level of Pollutant by Country (2023-2024)")
  ax2.set_xlabel('Country')
  ax2.set_ylabel('O3 Concentration (micrograms per cubic meter)')
  plt.xticks(rotation=90)
  st.pyplot(fig2)
else:
  airquality4=airquality.loc[airquality['pollutant']=='PM2.5', ['country', 'value']]
  grouped3=airquality4.groupby(['country'], as_index=False)['value'].mean()
  fig3=plt.figure()
  ax3=fig3.add_subplot()
  ax3.plot(grouped3['country'], grouped3['value'])
  ax3.set_title("Average Level of Pollutant by Country (2023-2024)")
  ax3.set_xlabel('Country')
  ax3.set_ylabel('PM2.5 Concentration (micrograms per cubic meter)')
  plt.xticks(rotation=90)
  st.pyplot(fig3)

st.markdown('___')
st.subheader("Besides the air we breathe, climate change impacts our weather patterns and therefore has a direct correlation with our spending, our homes, and for some their lives.")
st.text("In the US alone, billions of dollars are spent a year reparing the damage \ncaused by natural disasters.")

disaster_cost=pd.read_csv('https://raw.githubusercontent.com/mackenzieklein/CSVs-for-Final/main/events-US-1980-2023.csv')
disaster_cost['time_year']=disaster_cost['Weather and Climate Billion-Dollar Disasters to affect the U.S. from 1980-2023 (CPI-Adjusted)'].str.split('(').str.get(-1).str.replace(')', '')
disaster_cost['year']=disaster_cost['time_year'].str.split().str.get(-1)
del disaster_cost['time_year']
del disaster_cost['End Date']

with st.form(key='my_form'):
    dis_type = st.radio(
    "Please choose a disaster type",
    ('Tropical Cyclone', 'Drought', 'Freeze', 'Severe Storm', 'Winter Storm', 'Wildfire', 'Flooding'))
    submitted = st.form_submit_button(label='Show data')

    if submitted:
        disaster_cost = disaster_cost.loc[(disaster_cost['Disaster']==dis_type)]
        st.dataframe(disaster_cost)
        
st.markdown('___')
st.subheader("It's easy to dismiss natural disasters as a fluke of nature, but then why since 1901 are we seeing a steady increase in country wide precipitation levels?")
st.text("What we see below is an increasingly extreme deviation from the norm.")

precip_anom=pd.read_csv('https://raw.githubusercontent.com/mackenzieklein/CSVs-for-Final/main/precipitation_anomaly.csv')

ax=sns.regplot(x='Year', y='Anomaly (inches)', data=precip_anom, marker='x', line_kws=dict(color="orange"))
ax.figure.set_size_inches(8,6)
ax.set_xlabel('Year')
ax.set_ylabel('Precipitation Anomaly (inches)')
ax.set_title('Precipitation Anomaly in the USA (1901-2021)')
#st.pyplot(ax.get_figure()) was being impacted by above code so image inserted
st.image('precip.png')

st.markdown('___')
st.subheader("Most people will say environmental extremes will never effect them, but that is far from the truth.")
st.text("Each year thousands lose their homes and their lives due to natural disasters, \nand it could easily happen to anyone.")

col1, col2 = st.columns(2)
with col1:
  disaster_deaths=pd.read_csv('https://raw.githubusercontent.com/mackenzieklein/CSVs-for-Final/main/disas_deathstot_final.csv')
  disaster_deaths2=disaster_deaths.melt(id_vars=['country', 'lat', 'lon'],
                  var_name="year",
                  value_name="total_num")
  disaster_deaths2=disaster_deaths2.fillna(0)
  disaster_deaths2['total_num']=disaster_deaths2['total_num'].astype(float)
  disdeath=px.bar(disaster_deaths2, x='country', y='total_num', animation_frame='year', animation_group='country',
                    color='country', hover_name='country', range_y=[0,90000])
  disdeath.update_layout(title_text='Deaths Due to Natural Disasters (2000-2022)')
  disdeath.update_layout(showlegend=False)
  st.plotly_chart(disdeath, theme='streamlit', use_container_width=True)

with col2:
  homeless_dis=pd.read_csv('https://raw.githubusercontent.com/mackenzieklein/CSVs-for-Final/main/hmless_ndfinal.csv')
  homeless_dis2=homeless_dis.melt(id_vars=['country', 'lat', 'lon'],
                    var_name="year",
                    value_name="total_hmless")
  homeless_dis2=homeless_dis2.fillna(0)
  homeless_dis2['total_hmless']=homeless_dis2['total_hmless'].astype(float)
  homeless=px.bar(homeless_dis2, x='country', y='total_hmless', animation_frame='year', animation_group='country',
                    color='country', hover_name='country', range_y=[0, 5000000])
  homeless.update_layout(title_text='Homeless Due to Natural Disasters (2000-2022)')
  homeless.update_layout(showlegend=False)
  st.plotly_chart(homeless, theme='streamlit', use_container_width=True)
        
