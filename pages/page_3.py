import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import plotly.express as px
from streamlit_folium import folium_static
from streamlit_folium import st_folium

st.subheader("Now the big question, how far have we come?  Are we holding ourselves responsible to reach management goals?")
st.text("Data was presented showing how much wood was harvested, but what about how much acreage has \nbeen replanted? In the data below we can see many countries making a slow increase \nin their area of planted forest, showing a concentrated effort to replenish \nstripped land.")


forest_planted=pd.read_csv('https://raw.githubusercontent.com/mackenzieklein/CSVs-for-Final/main/plantedforest_area.csv')
forest_planted2=forest_planted.melt(id_vars=['country'],
        var_name="year",
        value_name="planted forest area")

forest_planted2['planted forest area']=forest_planted2['planted forest area'].astype(float)
forest_planted2['planted forest area']=forest_planted2['planted forest area']/1000

planted_world=px.bar(forest_planted2, x="country", y="planted forest area",animation_frame="year", animation_group="country",
          color="country", hover_name="country", range_y=[0,83600])
planted_world.update_layout(showlegend=False)
planted_world.update_layout(title_text='Area of Planted Forest in Thousand Hectares (2000-2019)')
st.plotly_chart(planted_world, theme='streamlit', use_container_width=True)

st.markdown('___')
st.subheader("In 2015 the UN introduced 17 Sustainable Development Goals, covering topics such as poverty, gender equality, economic growth, and climate action.")
st.text("These SDGs provide benchmark goals and guidelines for the world to improve quality \nof life for everyone. They provide a great resource to reflect on our efforts to \ncreate a better world.")

countries_drr=pd.read_csv('https://raw.githubusercontent.com/mackenzieklein/CSVs-for-Final/main/reportedDRR.csv')
countries_drr=countries_drr.loc[:, 'Indicator': '2023']

st.text("Target 1.5 aims to reduce exposure and vulnerability to climate-related and \nenvironmental disaster events. We already took a look at the death and homelessness \ncaused each year due to natural disasters, so you would hope this is an important \ngoal for all countries, right?")
st.text("The goal of this SDG is for all countries to have a Disaster Risk Reduction(DRR) \nstrategy in place to not only help their people, but also combat the escalation \nof major events.")
with st.form(key='my_form'):
    user_guess = st.slider('How many countries do you believe have a National Disaster Risk Reduction strategy?', 0, 195, 100)
    submitted = st.form_submit_button(label='Lock in my guess.')
    if submitted:
        st.write("As of 2023, 129 countries report having a National DRR strategy.")
        st.dataframe(countries_drr)

st.markdown('___')
st.text("129 out of 195 countries is larger than most would guess, but if we take it a step \nfurther and look at how many local governments have their own DRR strategies, \ndo you think we will see similar results?")

local_gov=pd.read_csv('https://raw.githubusercontent.com/mackenzieklein/CSVs-for-Final/main/localgov_DRR.csv')
local_gov['GeoAreaName'] = local_gov['GeoAreaName'].str.replace('United Kingdom of Great Britain and Northern Ireland', 'United Kingdom')
local_gov['GeoAreaName'] = local_gov['GeoAreaName'].str.replace('Republic of Korea', 'Korea')
local_gov['GeoAreaName'] = local_gov['GeoAreaName'].str.replace('Russian Federation', 'Russia')
local_gov['GeoAreaName'] = local_gov['GeoAreaName'].str.replace('United States of America', 'United States')

countries_url=("http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson")

localgov_map = folium.Map(location=[0, 0], zoom_start=2)

choro = folium.Choropleth(
    geo_data=countries_url,
    name="choropleth",
    data=local_gov,
    columns=["GeoAreaName", '2022'],
    key_on="feature.properties.name",
    fill_color="YlGn",
    fill_opacity=0.7,
    line_opacity=.1,
    legend_name="Percent of Local Government that Implements a DRR"
)
choro.add_to(localgov_map)
st_data=folium_static(localgov_map)

st.markdown('___')
st.text("It is not enough to report having a DRR strategy, the importance lies with how well \nthe country can implement it.  The UN scores each country on a scale of 0-1, \nallowing everyone to see areas needing improvement.")

country_rating=pd.read_csv('https://raw.githubusercontent.com/mackenzieklein/CSVs-for-Final/main/DRR_implementationscore.csv')
country_rating=country_rating.loc[:, 'GeoAreaName': '2022']
del country_rating['Units']
del country_rating['Reporting Type']
country_rating2=country_rating.melt(id_vars=['GeoAreaName'],
        var_name="year",
        value_name="rating")
country_rating2['GeoAreaName'] = country_rating2['GeoAreaName'].str.replace('United Kingdom of Great Britain and Northern Ireland', 'UK')
country_rating2['GeoAreaName'] = country_rating2['GeoAreaName'].str.replace('Republic of Korea', 'South Korea')
country_rating2['GeoAreaName'] = country_rating2['GeoAreaName'].str.replace('Russian Federation', 'Russia')
country_rating2['GeoAreaName'] = country_rating2['GeoAreaName'].str.replace('United States of America', 'USA')

rating=sns.catplot(data=country_rating2, x='rating', y='GeoAreaName', hue='year', jitter=False, palette='colorblind')
rating.set(title="UN's rating on country's DRR implementation (2021-2022)")
rating.set(xlabel='Rating (scale 0-1)')
rating.set(ylabel='Country')
sns.move_legend(rating, "upper left", bbox_to_anchor=(1, 1))
st.pyplot(rating.fig)

st.markdown('___')
st.subheader("The UN has also incorporated SDGs for companies, such as target 12.6 which encourages sustainable practices and for companies to report that information yearly.")
st.text("Since companies, especially large and transnational ones, play such a huge role in \nproduction and procurement, it is important for the public to have access to \ntheir progress towards sustainability.")
st.text("Do you think more companies will continue to adopt and report sustainable practices, \nor that the fear of profit loss is too high?")

company_sus=pd.read_csv('https://raw.githubusercontent.com/mackenzieklein/CSVs-for-Final/main/companies_susreport.csv')
company_sus=company_sus.loc[:, 'GeoAreaCode': '2022']
del company_sus['Activity']
del company_sus['Reporting Type']
del company_sus['Level of requirement']
del company_sus['Observation Status']
del company_sus['Units']
company_sus2=company_sus.melt(id_vars=['GeoAreaName', 'GeoAreaCode'],
        var_name="year",
        value_name="num_company")
company_sus2['GeoAreaName'] = company_sus2['GeoAreaName'].str.replace('United Kingdom of Great Britain and Northern Ireland', 'UK')
company_sus2['GeoAreaName'] = company_sus2['GeoAreaName'].str.replace('Republic of Korea', 'South Korea')
company_sus2['GeoAreaName'] = company_sus2['GeoAreaName'].str.replace('Russian Federation', 'Russia')
company_sus2['GeoAreaName'] = company_sus2['GeoAreaName'].str.replace('United States of America', 'USA')
company_sus2=company_sus2.fillna(0)
company_sus3=company_sus2.loc[company_sus2['GeoAreaName']!= 'World', :]
company=px.scatter(company_sus3, x="GeoAreaCode", y="num_company",animation_frame="year", animation_group="GeoAreaName",
           size='num_company', color="GeoAreaName", hover_name="GeoAreaName",
           size_max=55, range_y=[0,800])
company.update_layout(title_text='Number of Companies Publishing a Sustainability Report Per Country (2017-2022)')
st.plotly_chart(company, theme='streamlit', use_container_width=True)

st.markdown('___')
st.subheader("One of the most important SDGs for the future is target 12.8, which works to ensure people are educated on sustainability in development and their own lives.")
st.text("Climate change is not a quick fix, it took the world years to make the progress that \nwe can have seen.  Educating the youth in climate change and sustainability is \ncrucial for continued improvement and better ideas on how to tackle this issue \nwe created.")

sus_edu=pd.read_csv('https://raw.githubusercontent.com/mackenzieklein/CSVs-for-Final/main/susedu_index.csv')
sus_edu=sus_edu.loc[:, 'GeoAreaName': '2020']
del sus_edu['Reporting Type']
del sus_edu['Units']
sus_edu2=sus_edu.melt(id_vars=['GeoAreaName'],
        var_name="year",
        value_name="index")
sus_edu2['GeoAreaName'] = sus_edu2['GeoAreaName'].str.replace('United Kingdom of Great Britain and Northern Ireland', 'UK')
sus_edu2['GeoAreaName'] = sus_edu2['GeoAreaName'].str.replace('Republic of Korea', 'South Korea')
sus_edu2['index']=sus_edu2['index']*100
fig=plt.figure()
ax=fig.add_subplot()
ax.plot(sus_edu2['GeoAreaName'], sus_edu2['index'])
ax.set_title("Percent of Education with Sustainability in Curriculum (2020)")
ax.set_xlabel('Country')
ax.set_ylabel('Percent')
plt.xticks(rotation=90)
st.pyplot(fig)
