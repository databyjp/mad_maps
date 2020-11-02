# ========== (c) JP Hwang 12/7/20  ==========

import logging

# ===== START LOGGER =====
logger = logging.getLogger(__name__)
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
sh = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh.setFormatter(formatter)
root_logger.addHandler(sh)

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

desired_width = 320
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', desired_width)

data_df = pd.read_csv("srcdata/proc_data.csv", index_col=0)
data_df['fips'] = data_df['fips'].astype(str).apply(lambda x: "0" * (5-len(x)) + x)

# Load county data
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

# ==============================
# ===== DATAVIZ - GEO DATA =====
# ==============================
labels = {
    "log_pop": "Population (log 10)",
    "PCTPOVALL_2018": "Population Living in Poverty (%)",
    "Unemployment_rate_2018": "Unemployment Rate (%)",
    "Median_Household_Income_2018": "Typical (Median)<BR>Household Income (USD)",
    "state": "State",
    "POP_ESTIMATE_2018": "Population",
}

# Map showing income levels by county
fig = px.choropleth_mapbox(data_df, locations="fips", color="Median_Household_Income_2018",
                           range_color=[0, 100000],
                           geojson=counties, color_continuous_scale=px.colors.diverging.RdYlBu, labels=labels)
fig.update_layout(coloraxis_colorbar=dict(
    tickvals=[0, 20000, 40000, 60000, 80000, 100000],
    ticktext=["0", "20k", "40k", "60k", "80k", "100k+"]
))
fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=3.9, mapbox_center={"lat": 37.0902, "lon": -95.7129},
                  margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.update_traces(marker=dict(line=dict(width=0.3, color="gray")))
fig.show()

# ========== MAP A FILTERED SET ==========
# Map showing counties with typical income < 40k
tmp_df = data_df[data_df["Median_Household_Income_2018"] < 40000]
fig = px.choropleth_mapbox(tmp_df, locations="fips", color="Median_Household_Income_2018",
                           range_color=[0, 100000],
                           geojson=counties, color_continuous_scale=px.colors.diverging.RdYlBu, labels=labels)
fig.update_layout(coloraxis_colorbar=dict(
    tickvals=[0, 20000, 40000, 60000, 80000, 100000],
    ticktext=["0", "20k", "40k", "60k", "80k", "100k+"]
))
fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=3.9, mapbox_center={"lat": 37.0902, "lon": -95.7129},
                  margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.update_traces(marker=dict(line=dict(width=0.3, color="gray")))
fig.show()

fig = px.choropleth_mapbox(tmp_df, locations="fips", color="Median_Household_Income_2018",
                           range_color=[20000, 40000],
                           geojson=counties, color_continuous_scale=px.colors.sequential.Oranges[::-1], labels=labels)
fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=3.9, mapbox_center={"lat": 37.0902, "lon": -95.7129},
                  margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.update_traces(marker=dict(line=dict(width=0.3, color="gray")))
fig.show()

# Map showing counties with typical income < 70k
tmp_df = data_df[data_df["Median_Household_Income_2018"] > 70000]
fig = px.choropleth_mapbox(tmp_df, locations="fips", color="Median_Household_Income_2018",
                           range_color=[0, 100000],
                           geojson=counties, color_continuous_scale=px.colors.diverging.RdYlBu, labels=labels)
fig.update_layout(coloraxis_colorbar=dict(
    tickvals=[0, 20000, 40000, 60000, 80000, 100000],
    ticktext=["0", "20k", "40k", "60k", "80k", "100k+"]
))
fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=3.9, mapbox_center={"lat": 37.0902, "lon": -95.7129},
                  margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.update_traces(marker=dict(line=dict(width=0.3, color="gray")))
fig.show()

fig = px.choropleth_mapbox(tmp_df, locations="fips", color="Median_Household_Income_2018",
                           geojson=counties, color_continuous_scale=px.colors.sequential.Blues, labels=labels)
fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=3.9, mapbox_center={"lat": 37.0902, "lon": -95.7129},
                  margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.update_traces(marker=dict(line=dict(width=0.3, color="gray")))
fig.show()
# ========== GROUP COUNTIES BY POPULATION SIZE ==========
names = ['1 quartile', '2 quartile', '3 quartile', '4 quartile']
x = pd.qcut(data_df["POP_ESTIMATE_2018"], 4, labels=names)
tmp_df = data_df.assign(pop_bin=x)
tmp_df = tmp_df[tmp_df.pop_bin.notna()]

fig = px.choropleth(geojson=counties, locations=tmp_df.fips, scope="usa",
                    color=tmp_df.pop_bin, color_discrete_sequence=px.colors.sequential.Sunsetdark,
                    labels={"color": "Counties by<BR>population"},
                    category_orders={"color": names})
fig.show()

# ========== Bar Plot  ==========
bins = [0, 10000, 25000, 65000, np.inf]
names = ['<10k', '10k-25k', '25k-65k', '65k+']
x = pd.cut(tmp_df["POP_ESTIMATE_2018"], bins=bins, labels=names)
tmp_df = data_df.assign(pop_bin=x)

bins = [0, 40000, 50000, 60000, 70000, 80000, np.inf]
names = ['<40k', '40k-50k', '50k-60k', '60k-70k', '70k-80k', '80k+']
x = pd.cut(tmp_df["Median_Household_Income_2018"], bins=bins, labels=names)
tmp_df = tmp_df.assign(income_bin=x)

grp_df = tmp_df.groupby(["income_bin", "pop_bin"]).agg(["mean", "count"])["PCTPOVALL_2018"].reset_index()
fig = px.bar(
    grp_df, x="income_bin", y="mean", barmode="group", title="Differences in Poverty Rates - Large vs Small Counties",
    category_orders={"pov_income": names},
    labels={"income_bin": "Typical Household Income ($)", "mean": "Average poverty rate (%)", "pop_bin": "County population"},
    color="pop_bin",
    color_discrete_sequence=px.colors.sequential.Bluyl,
    template="plotly_white",
)
fig.update_traces(marker=dict(line=dict(width=0.5, color="Silver")))
fig.show()

# ========== Scatter map  ==========
# Get center coordintes for each FIPS

county_data_list = list()
for tmp in counties["features"]:
    tmp_fips = tmp["id"]
    if tmp["geometry"]["type"] == 'Polygon':
        tmp_crds = tmp["geometry"]["coordinates"][0]
    elif tmp["geometry"]["type"] == 'MultiPolygon':
        tmp_crds = tmp["geometry"]["coordinates"][0][0]
    else:
        print(tmp["geometry"]["type"])
        print(tmp["geometry"]["coordinates"])
    x_crds = [i[0] for i in tmp_crds]
    y_crds = [i[1] for i in tmp_crds]
    center_crds = [(min(x_crds)+max(x_crds))/2, (min(y_crds)+max(y_crds))/2]
    data_dict = {"fips": tmp_fips, "lon": center_crds[0], "lat": center_crds[1]}
    county_data_list.append(data_dict)
county_df = pd.DataFrame(county_data_list)

# Merge income data & plot
county_df = county_df.join(data_df[["fips", "Median_Household_Income_2018", "POP_ESTIMATE_2018"]].set_index("fips"), on="fips", how="left")
county_df["POP_ESTIMATE_2018"].fillna(0, inplace=True)

fig = px.scatter_mapbox(county_df, lat="lat", lon="lon", color="Median_Household_Income_2018", size="POP_ESTIMATE_2018",
                        range_color=[40000, 70000], size_max=40,
                        color_continuous_scale=px.colors.diverging.RdYlBu, labels=labels
                        )
fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=3.9, mapbox_center={"lat": 37.0902, "lon": -95.7129},
                  margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.show()
