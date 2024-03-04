import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from iso3166 import countries

import plotly.io as pio
pio.renderers.default='browser'

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from sklearn.preprocessing import LabelEncoder

import warnings
warnings.filterwarnings("ignore")



#Read and Data Analyze

df = pd.read_csv("space_corrected.csv")
df.head()

describe = df.describe()

df.info()

#Number of Launches by Every Company
    
    ds = df["Company Name"].value_counts().reset_index()[:28]
    ds


fig = go.Figure(go.Bar(x = ds["index"], y = ds["Company Name"],
                       marker = dict(color=ds["Company Name"],
                                    colorscale = "bluered")))
fig.update_layout(title="Number of Launches by Every Company", xaxis_title="Top 28 Country", yaxis_title ="count",hovermode ="x")
fig.show()


# Rocket Status

ds = df["Status Rocket"].value_counts().reset_index()
ds

fig = px.pie(ds, values= "Status Rocket", names= "index",title="Rocket Status")
fig.show()

# Mission Status

ds = df["Status Mission"].value_counts().reset_index()[:3]
ds

fig = px.bar(ds, x ="index", y="Status Mission", title="Mission Status")
fig.show()

# Rocket Cost Distribution with Rocket Status

np.sum(pd.isna(df.loc[:," Rocket"]))

df_ = df.dropna(subset=[" Rocket"],axis= "rows")
len(df_)

np.sum(pd.isna(df_.loc[:," Rocket"]))

df_.loc[:, " Rocket"]

df_.loc[:," Rocket"] = df_.loc[:," Rocket"].fillna(0.0).str.replace(",","")
df_.loc[:," Rocket"] = df_.loc[:," Rocket"].astype(np.float64).fillna(0.0)

df_d = df_[df_.loc[:, " Rocket"]< 1000]
plt.figure(figsize = (22,6))
sns.histplot(data = df_d, x = " Rocket", hue = "Status Rocket")
plt.show()

# Rocket Cost Distribution with Mission Status

np.sum(pd.isna(df.loc[:,"Status Mission"]))

plt.figure(figsize = (22,6))
sns.histplot(data = df_d, x = " Rocket", hue = "Status Mission")
plt.show()

# Total Spent Money for each Companies

df_.head()

df_.groupby(["Company Name"])[" Rocket"].sum().reset_index()

df_money = df_.groupby(["Company Name"])[" Rocket"].sum().reset_index()
df_money = df_money[df_money[" Rocket"]>0]
df_money.head()

df_money_ = df_money.sort_values(by= [" Rocket"],ascending=False)[:15]
df_money_.head()    

fig = px.bar(df_money_ ,x = "Company Name", y =" Rocket", title="Total Spent Money for each Company")
fig.show()

# Mission Number by Years

df["date"] = pd.to_datetime(df["Datum"])
df.head()

df["year"] = df["date"].apply(lambda datetime: datetime.year)
df.head()

ds = df["year"].value_counts().reset_index()
ds

fig = px.bar(ds, x ="index", y="year",title="Missions Number by Year")
fig.show()


# Countries and Mission Status

encoder = LabelEncoder()
encoder.fit(df["Status Mission"])
encoder

colors = {0: "Red",
          1: "Orange",
          2: "Yellow",
          3: "Green"}
colors


countries_dict = {
    "Russia" : "Russian Federation",
    "New Mexico" : "USA",
    "Yellow Sea" : "China",
    "Shahrud Missile Test Site" : "Iran",
    "Pacific Missile Range Facility" : "USA",
    "Barents Sea" : "Russian Federation",
    "Gran Canaria" : "USA"
}
df["country"] = df["Location"].str.split(", ").str[-1].replace(countries_dict)
df.head()

fig = make_subplots(rows=4, cols=4, subplot_titles=df["country"].unique())
for i, country in enumerate(df["country"].unique()):
    counts = df[df["country"] == country]["Status Mission"].value_counts(normalize=True)*100
    color = [colors[x] for x in encoder.transform(counts.index)]
    trace = go.Bar(x = counts.index, y=counts.values, name=country,marker={"color": color}, showlegend=False)
    fig.add_trace(trace, row=(i//4)+1, col =(i%4)+1)
fig.update_layout(title = {"text":"Countries and Mission Status"})
for i in range(1,5):
    fig.update_yaxes(title_text = "Percentage", row = i, col=1)
fig.show()

# Sunburst Chart Analysis

sun = df.groupby(["country","Company Name","Status Mission"])["Datum"].count().reset_index()
sun.head()


sun = sun[(sun.country == "USA") | (sun.country == "China") | (sun.country == "Russian Federation") | (sun.country == "France")]
sun.head()


fig = px.sunburst(sun, path=["country","Company Name","Status Mission"],values="Datum",title="Sunburst Chart for some Countries")
fig.show()


# Status Mission by Countries in World Map

country_dict = dict()
for c in countries:
    country_dict[c.name] = c.alpha3

df["alpha3"] = df["country"]
df = df.replace({
    "alpha3":country_dict})
df.loc[df["country"] == "North Korea", "alpha3"] = "PRK"
df.loc[df["country"] == "South Korea", "alpha3"] = "KOR"
df.head()

mapdf = df.groupby(["country", "alpha3"])["Status Mission"].count().reset_index()
mapdf.head()

fig = px.choropleth(mapdf,locations="alpha3",hover_name="country",color="Status Mission", title="Status Mission by Countries")
fig.show()






















