
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

from copy import deepcopy

path = "mpg.csv"

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df

mpg_df_raw = load_data(path)
mpg_df = deepcopy(mpg_df_raw)

st.title("Introduction to Streamlit")
st.header("MPG Data Exploration")

# st.table(mpg_df)
if st.checkbox("Show Dataframe"):
    st.subheader("This is my dataset:")
    st.dataframe(mpg_df)

left_column, middle_column, right_column = st.columns([3,1,1])
# 3 + 1 + 1 = 5
# first column: 3/5 of the total space

years = ["All"] + sorted(pd.unique(mpg_df["year"]))
year = left_column.selectbox("Choose a year", years)

show_means = middle_column.radio("Show Class Means", ["Yes","No"])

if year == "All":
    reduced_df = mpg_df
else:
    reduced_df = mpg_df[mpg_df["year"] == year]

means = reduced_df.groupby("class").mean(numeric_only=True)

st.dataframe(reduced_df)
m_fig, ax = plt.subplots(figsize =(10,8))
ax.scatter(reduced_df["displ"], reduced_df["hwy"], alpha=0.7)
ax.set_xlabel("Displacement")
ax.set_ylabel("Highway MPG")
ax.set_title("Displacement vs. Highway MPG")
if show_means == "Yes":
    for i, row in means.iterrows():
        ax.scatter(row["displ"], row["hwy"], s=100, label=i, edgecolor="black")
    ax.legend(title="Class")
st.pyplot(m_fig)

p_fig = px.scatter(reduced_df, x="displ", y="hwy", color="class", title="Displacement vs. Highway MPG")
if show_means == "Yes":

    p_fig.add_traces(px.scatter(means, x=means["displ"], y=means["hwy"], color=means["class"]).data)
st.plotly_chart(p_fig)