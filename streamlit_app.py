import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import plotly.express as px
from streamlit_folium import folium_static
from streamlit_folium import st_folium

st.title("Analyzing the World's Response to Climate Change")
st.markdown('___')

threat=pd.read_csv('https://raw.githubusercontent.com/mackenzieklein/CSVs-for-Final/main/threat.csv')
somewhat_threat=pd.read_csv('https://raw.githubusercontent.com/mackenzieklein/CSVs-for-Final/main/somewhat_threat.csv')
serious_threat=pd.read_csv('https://raw.githubusercontent.com/mackenzieklein/CSVs-for-Final/main/serious_threat.csv')

st.subheader("The world's first climate conference was held in 1979, with the UN forming the Intergovernmental Panel on Climate Change (IPCC) as early as 1988.\n Since then, the issue of climate change has been a controversial topic, always displayed in extremes.  It seems to be one of those topics either always on the front page or pushed under the rug.")
st.text("Over the past 45 years, do you think we've made a difference?  Seen any progress \ntowards change?  How have your views, and the world's, changed over the years?")

with st.form(key='my_form'):
    option = st.radio(
        'How do you view the issue of climate change?',
        ('Serious threat', 'Somewhat serious threat', 'A threat, but not that serious'))
    submitted=st.form_submit_button(label='Show how your opinion compares to the world.')
         
    if submitted:
        if option == 'Serious threat':
            s_threat=sns.catplot(data=serious_threat, x='per_pop', y='country', hue='year', jitter= False, palette='colorblind')
            s_threat.set(title='Percent of population that see climate change as a serious threat (by country)')
            s_threat.set(xlabel='Percent Population (%)')
            s_threat.set(ylabel='Country')
            st.pyplot(s_threat.fig)
        elif option == 'Somewhat serious threat':
            ss_threat=sns.catplot(data=somewhat_threat, x='Per_pop', y='country', hue='Year', jitter= False, palette='colorblind')
            ss_threat.set(title='Percent of population that see climate change as a somewhat serious threat (by country)')
            ss_threat.set(xlabel='Percent Population (%)')
            ss_threat.set(ylabel='Country')
            st.pyplot(ss_threat.fig)
        else:
            threat_gr=sns.catplot(data=threat, x='per_pop', y='country', hue='year', jitter= False, palette='colorblind')
            threat_gr.set(title='Percent of population that see climate change as a threat (by country)')
            threat_gr.set(xlabel='Percent Population (%)')
            threat_gr.set(ylabel='Country')
            st.pyplot(threat_gr.fig)
             
st.markdown('___')

st.subheader("When someone mentions climate change causes, usually two things come to mind: deforestation and greenhouse gas.  Let's examine how some countries around the world are tackling these two contributing factors.")
st.text("Below we can see how much wood was removed by countries only for production \nof goods and services not including anything used for energy.")

wood_removal=pd.read_csv('https://raw.githubusercontent.com/mackenzieklein/CSVs-for-Final/main/woodremovalcubicmeters_final.csv')

wood_removal['country'] = wood_removal['country'].str.replace('UK', 'United Kingdom')
wood_removal['country'] = wood_removal['country'].str.replace('South Korea', 'Korea')
wood_removal['country'] = wood_removal['country'].str.replace('USA', 'United States')

countries_url=("http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson")

wood_map = folium.Map(location=[0, 0], zoom_start=2)

choro = folium.Choropleth(
    geo_data=countries_url,
    name="choropleth",
    data=wood_removal,
    columns=["country", 'removal_cm'],
    key_on="feature.properties.name",
    fill_color="YlGn",
    fill_opacity=0.7,
    line_opacity=.1,
    legend_name="2011 Wood Removal in Cubic Meters"
            )
choro.add_to(wood_map)
for index,row in wood_removal.iterrows():
    tooltip='Click me'
    loc=[row['lat'], row['lon']]
    label=row['country']
    m=folium.Marker(location=loc, popup=label, tooltip=tooltip)
    m.add_to(wood_map)

st_data=folium_static(wood_map)

st.markdown('___')
st.text("As a general trend, we can see that many countries have been lowering their \ncarbon footprint over the years. Some say it's too little too late, \nothers would argue it hinders future development.")

co_percapita=pd.read_csv('https://raw.githubusercontent.com/mackenzieklein/CSVs-for-Final/main/co2_percapita.csv')

world_co=co_percapita.loc[co_percapita['country']!= 'USA', :]
world_co2=world_co.melt(id_vars=['country'], var_name='year', value_name='co2_percapita')
filtered_world_co2=world_co2.loc[world_co2['year']>='2000']
world=px.bar(filtered_world_co2, x='country', y='co2_percapita', animation_frame='year', animation_group='country',
            color='country', hover_name='country',range_y=[0,50])
world.update_layout(title_text='World CO2 per capita emissions (2000-2022)')
world.update_layout(showlegend=False)
st.plotly_chart(world, theme='streamlit', use_container_width=True)

st.markdown('___')
st.text("Focusing in on the US allows for a firsthand view on how the climate movement has \nimpacted the country's carbon dioxide emissions.")

co_percapita=pd.read_csv('https://raw.githubusercontent.com/mackenzieklein/CSVs-for-Final/main/co2_percapita.csv')

us_co=co_percapita.loc[co_percapita['country']=='USA', :]
us_co2=us_co.melt(id_vars=['country'], var_name='year', value_name='co2_percapita')
us_co2['year']=us_co2['year'].astype(float)
usa_co2=sns.regplot(data=us_co2, x='year', y='co2_percapita', marker='x', line_kws=dict(color="orange"))
plt.xticks(rotation=90)
usa_co2.set(title='US CO2 per capita emissions (1992-2022)')
usa_co2.set(xlabel='Year')
usa_co2.set(ylabel='CO2 Emissions')
#st.pyplot(usa_co2.get_figure()) code was impacted by above so figure was altered when submit button was pressed, so image inserted
st.image('us_co2.png')




