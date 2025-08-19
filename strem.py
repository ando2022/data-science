
import streamlit as st
import matplotlib.pyplot as plt
from urllib.request import urlopen
import json
import pandas as pd
from pathlib import Path
import plotly.express as px

data_folder = Path("my-first-streamlitapp/")
volcano_ds =  "volcano_ds_pop.csv"
geojson_file = "countries.geojson"
df = pd.read_csv(volcano_ds)

if st.checkbox("Show Dataframe"):
    st.subheader("This is my dataset:")
    st.dataframe(df)

left_column, middle_column, right_column = st.columns([3,1,1])

max_per_region = df.groupby("Country")["Population (2020)"].max()
countries = df["Country"].unique()
country = left_column.selectbox("Choose a country", countries)
show_max_per_region = middle_column.radio("Show Most Populated Areas with volcanos", ["Yes","No"])

with open(geojson_file) as f:
    geojson = json.load(f)

fig = px.scatter_map(
    df,
    lat="Latitude",
    lon="Longitude",
    size="Population (2020)",
    hover_name="Volcano Name",
    hover_data=["Country", "Elev"],
    zoom=1,
    title="All Volcanoes"
)

st.plotly_chart(fig)

df_volcanoes = df.groupby("Country").size().reset_index(name='Volcano Count')
# small df: Country + Population (2020) max per country
max_per_region = df.groupby("Country")["Population (2020)"].max().reset_index()

# choose ONE volcano per country (highest elevation)
df_unique = (
    df.sort_values(["Country", "Elev"], ascending=[True, False])
      .drop_duplicates(subset=["Country"])  # now 1 row per Country
      [["Country", "Population (2020)", "Volcano Name", "Latitude", "Longitude", "Elev"]]
)

# merge into the SMALL df; row count stays the same
merged = max_per_region.merge(
    df_unique,
    on=["Country", "Population (2020)"],
    how="left",
    validate="one_to_one"        # raises if keys aren’t unique
)

rows = merged[merged["Country"] == country]

out = rows[["Country","Volcano Name","Latitude","Longitude","Population (2020)"]]


if show_max_per_region == "Yes":
    fig = px.scatter_map(
        merged[merged["Country"] == country],   # use merged df with max pop values
        lat="Latitude",
        lon="Longitude",
        size="Population (2020)",
        hover_name="Volcano Name",
        hover_data=["Country", "Elev"],
        zoom=2,
        title=f"Most Populated Area in {country} with Volcanoes"
    )

fig.update_layout(mapbox_style="open-street-map")  # optional background
st.plotly_chart(fig)

df_volcanoes = df.groupby("Country").size().reset_index(name='Volcano Count')

fig_2 = px.choropleth_map(
    df_volcanoes,
    color="Volcano Count",
    geojson=geojson,
    locations="Country",
    featureidkey="properties.ADMIN",
    center={"lat": 46.8, "lon": 8.3},
    map_style="open-street-map", 
    zoom=1.5,
    opacity=0.8,
    width=1600,
    height=1000,
    title="Absolute Number of Volcanos by Country",
    color_continuous_scale="Magenta",
    labels={"Volcano Count": "Number of Volcanoes"}
)


st.plotly_chart(fig_2)