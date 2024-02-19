# Imports
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title('NBA Player Stats Explorer')

st.markdown("""
    This app performs simple webcraping of NBA player stats data!
    * **Python libraries:** base64, pandas, streamlit
    * **Data source:** [Basketball-reference.com](https://www.basketball-reference.com/).
""")

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950,2025)))) # The 'reversed()' was used to make 2019 the first year appearing on the select box

# Web scraping of NBA player stats
@st.cache_data
def lead_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    html = pd.read_html(url, header=0) # I had a problem here. Solution: https://stackoverflow.com/questions/68275857/urllib-error-urlerror-urlopen-error-ssl-certificate-verify-failed-certifica
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index) # Deletes repeating headers in content
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
    return playerstats

playerstats = lead_data(selected_year)

# Sidebar - Team selection
sorted_unique_team = sorted(playerstats.Tm.unique()) # 'playerstats.Tm.unique()' return unique team names from the dataframe and 'sorted()' show it at 'Team' select box in alphabetical order
seleted_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

# Sidebar - Position selection
#unique_pos = sorted(playerstats.Pos.unique())
unique_pos = ['C', 'PF', 'SF', 'PG', 'SG']
                                    #the name  | Possibles values | Default values
#selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos[:1]) # <-  show the first value of de data (C) as the default value
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

# Filtering data
df_selected_team = playerstats[(playerstats.Tm.isin(seleted_team)) & (playerstats.Pos.isin(selected_pos))]

st.header('Display Player Stats of Selected Team(s)')
st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
st.dataframe(df_selected_team)

# Download NBA player stats data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

# Heatmap
if st.button('Intercorrelation Heatmap'):
    st.header('Intercorrelation Matrix Heatmap')
    #$df_selected_team.to_csv('output.csv',index=False)
    #$df = pd.read_csv('output.csv')

    # Filter out non-numeric columns 
    #test = df_selected_team.map(type)
    #test
    str_columns = ['Player', 'Pos', 'Tm']
    for column in df_selected_team.columns:
        if column not in str_columns:
            df_selected_team[column] = df_selected_team[column].astype(float)
        else:
            df_selected_team[column] = df_selected_team[column].astype(str)

    numeric_cols_only = df_selected_team[df_selected_team.select_dtypes(include=[int, float]).columns]
    #numeric_cols_only
    ## Calculate correlation
    corr = numeric_cols_only.corr()
    #corr
    ## Create a mask for the upper triangle
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True

    ## Plot heatmap
    with sns.axes_style("white"):
        fig, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
    st.pyplot(fig)