import pandas as pd
import streamlit as st
import base64
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


st.title("NFL Football Player Stats Explorer")

st.markdown(""" 
This app performs simple web scraping of NFL Football Player stats data!
* **Python Libraries:** base64, pandas, streamlit 
* **Data Source:** [Football-Referance.com](https://www.pro-football-reference.com/) 
""")

st.sidebar.header("User Input Features")
selected_year = st.sidebar.selectbox("Year", list(reversed(range(1990,2021))))


# create data

def load_data(year):
    url = 'https://www.pro-football-reference.com/years/' + str(year) + '/rushing.htm'
    html = pd.read_html(url, header=1)
    df = html[0] # it means the first dataframe of html that is our website data
    raw = df.drop(df[df.Age=="Age"].index) # deletes repeating headers in the website content
    raw = raw.fillna(0)
    data = raw.drop(["Rk"], axis=1)
    return data

data = load_data(selected_year)

# sidebar team selection
unique_teams = sorted(data.Tm.unique())
selected_team = st.sidebar.multiselect("Team", unique_teams, unique_teams)


# sidebar position selection
unique_position = ["RB", "QB", "WR", "FB", "TE"]
selected_pos = st.sidebar.multiselect("Position", unique_position, unique_position[:1])



# filtering data
df_filtered_teams = data[(data.Tm.isin(selected_team)) & (data.Pos.isin(selected_pos))]

st.header("Display Player Stats Of Selected Teams :")
st.write("Data Dimension:  " + str(df_filtered_teams.shape[0]) + " Rows and "+ str(df_filtered_teams.shape[1]) + " Columns.")
st.dataframe(df_filtered_teams)

# download the user data
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href = "data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_filtered_teams), unsafe_allow_html=True)


# create heatmap
if st.button("Intercorrelation Heatmap"):
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.header("Intercorrelation Matrix Heatmap")
    df_filtered_teams.to_csv("output.csv", index=False)
    df = pd.read_csv("output.csv")

    corr = df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True 
    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(7,5))
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
    st.pyplot()






