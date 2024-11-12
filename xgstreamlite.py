import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg


st.write("""
# Ligue 1 xG against vs xG
Who is the best club in ligue 1 ?!?
""")





def get_logo_path(squad_name):
    # Remplacez ce chemin par le chemin où vous stockez vos logos
    return f"./image/{squad_name}.png" 

def plot_with_logos(x, y, names, ax):
    for x0, y0, name in zip(x, y, names):
        logo_path = get_logo_path(name)
        img = mpimg.imread(logo_path)
        imagebox = OffsetImage(img, zoom=0.8)  # Ajustez le zoom selon la taille des logos
        ab = AnnotationBbox(imagebox, (x0, y0), frameon=False, pad=0.5)
        ax.add_artist(ab)

def plot_with_logos_andplayernames(x, y, names, player_names, ax):
    for x0, y0, name, player_name in zip(x, y, names, player_names):
        # Charger et afficher le logo
        logo_path = get_logo_path(name)
        img = mpimg.imread(logo_path)
        imagebox = OffsetImage(img, zoom=0.8)  # Ajustez le zoom selon la taille des logos
        ab = AnnotationBbox(imagebox, (x0, y0), frameon=False, pad=0.5)
        ax.add_artist(ab)
        
        # Ajouter le nom du joueur à côté du logo
        ax.text(x0, y0 - 0.3, player_name, ha='center', fontsize=8)  # Ajustez la position si nécessaire

@st.cache_data
def load_data():
    df = pd.read_html('https://fbref.com/en/comps/13/Ligue-1-Stats', attrs={"id":"results2024-2025131_overall"})[0]
    dfrcsa = pd.read_html('https://fbref.com/en/squads/c0d3eab4/Strasbourg-Stats', attrs={"id":"stats_standard_13"})[0]
    dfmonaco = pd.read_html('https://fbref.com/en/squads/fd6114db/Monaco-Stats', attrs={"id":"stats_standard_13"})[0]
    dfparis = pd.read_html('https://fbref.com/en/squads/e2d8892c/Paris-Saint-Germain-Stats', attrs={"id":"stats_standard_13"})[0]
    dfMarseille = pd.read_html('https://fbref.com/en/squads/5725cc7b/Marseille-Stats', attrs={"id":"stats_standard_13"})[0]
    dfNice = pd.read_html('https://fbref.com/en/squads/132ebc33/Nice-Stats', attrs={"id":"stats_standard_13"})[0]
    dfLille = pd.read_html('https://fbref.com/en/squads/cb188c0c/Lille-Stats', attrs={"id":"stats_standard_13"})[0]
    dfLyon = pd.read_html('https://fbref.com/en/squads/d53c0b06/Lyon-Stats', attrs={"id":"stats_standard_13"})[0]

    dfrcsa2 = dfrcsa[(dfrcsa['Unnamed: 0_level_0','Player']!='Squad Total') & (dfrcsa['Unnamed: 0_level_0','Player']!='Opponent Total')]
    dfmonaco2 = dfmonaco[(dfmonaco['Unnamed: 0_level_0','Player']!='Squad Total') & (dfmonaco['Unnamed: 0_level_0','Player']!='Opponent Total')]
    dfparis2 = dfparis[(dfparis['Unnamed: 0_level_0','Player']!='Squad Total') & (dfparis['Unnamed: 0_level_0','Player']!='Opponent Total')]
    dfMarseille2 = dfMarseille[(dfMarseille['Unnamed: 0_level_0','Player']!='Squad Total') & (dfMarseille['Unnamed: 0_level_0','Player']!='Opponent Total')]
    dfNice2 = dfNice[(dfNice['Unnamed: 0_level_0','Player']!='Squad Total') & (dfNice['Unnamed: 0_level_0','Player']!='Opponent Total')]
    dfLille2 = dfLille[(dfLille['Unnamed: 0_level_0','Player']!='Squad Total') & (dfLille['Unnamed: 0_level_0','Player']!='Opponent Total')]
    dfLyon2 = dfLyon[(dfLyon['Unnamed: 0_level_0','Player']!='Squad Total') & (dfLyon['Unnamed: 0_level_0','Player']!='Opponent Total')]
    
    dfrcsa2['teamname'] = 'Strasbourg'
    dfmonaco2['teamname'] = 'Monaco'
    dfparis2['teamname'] = 'Paris S-G'
    dfMarseille2['teamname'] = 'Marseille'
    dfNice2['teamname'] = 'Nice'
    dfLille2['teamname'] = 'Lille'
    dfLyon2['teamname'] = 'Lyon'

    return df, dfrcsa2, dfmonaco2, dfparis2, dfMarseille2, dfNice2, dfLille2, dfLyon2

df, dfrcsa2, dfmonaco2, dfparis2, dfMarseille2, dfNice2, dfLille2, dfLyon2 = load_data()

df_all_player_ligue1 = pd.concat([dfrcsa2, dfmonaco2, dfparis2, dfMarseille2, dfNice2, dfLille2, dfLyon2], ignore_index=True)
def extract_year(age_str):
    try:
        return int(age_str.split('-')[0])
    except (AttributeError, ValueError):
        return np.nan  # Ou une valeur par défaut

dfcolorsbyteam = df_all_player_ligue1[('teamname')].sort_values().unique()
print(dfcolorsbyteam)
df_all_player_ligue1[('Unnamed: 3_level_0', 'Age')] = df_all_player_ligue1[('Unnamed: 3_level_0', 'Age')].apply(extract_year)

dfselect = pd.DataFrame({'choix':["xGA","Goals"]})
graph_select = st.selectbox("Choix du graph a afficher :",dfselect['choix'],index=None)


if graph_select == "xGA":
    #courbe xG vs xGA
    x2 = df['xG']
    y2 = df['xGA']
    name = df['Squad'] 
    # plot
    fig, ax = plt.subplots(figsize=(10,10))
    # Scatter plot
    sc2 = ax.scatter(x2, y2, color='grey')  # use a neutral color for points
    # Calculate mean values
    moyennex = x2.mean()
    moyenney = y2.mean()
    x2_line = np.linspace(min(x2.min()-4, y2.min())-4, max(x2.max(), y2.max()), 100)
    ax.plot(x2_line, x2_line, label='y = x', color='black')  # Line plot y=x

    # Add mean lines
    ax.axvline(x=moyennex, color='red', linestyle='--')  # Vertical line at mean xG
    ax.axhline(y=moyenney, color='blue', linestyle='--')  # Horizontal line at mean xGA

    ax.fill_between(x=[0, moyennex], y1=moyenney, color='yellow', alpha=0.1)  # Below avg xG and xGA
    ax.fill_between(x=[moyennex, max(x2)+2], y1=moyenney, color='green', alpha=0.1)  # Below avg xG and xGA
    ax.fill_betweenx(y=[moyenney,max(y2)+6], x1=moyennex, color='red', alpha=0.1)  # Below avg xG and xGA
    ax.fill_betweenx(y=[moyenney,max(y2)+6], x1=moyennex,x2=max(x2)+2, color='blue', alpha=0.1)  # Below avg xG and xGA

    # Annotate each point
    plot_with_logos(x2, y2, name, ax)

    # Set labels and legend
    ax.set_xlabel('xG')
    ax.set_ylabel('xGA')
    ax.legend(['y = x', 'Mean xG', 'Mean xGA'], loc='upper left')

    st.pyplot(fig)
elif graph_select == "Goals":
    x = df['xG']
    y= df['GF']
    name = df['Squad']
    # plot
    fig, ax = plt.subplots(figsize=(10,10))

    sc = ax.scatter(x, y)


    x_line = np.linspace(min(x.min(), y.min()), max(x.max(), y.max()), 100)
    ax.plot(x_line, x_line, color='black')  # Line plot y=x

    plot_with_logos(x, y, name, ax)
    ax.legend()
    ax.set_xlabel('xG')
    ax.set_ylabel('GF')

    st.pyplot(fig)



dfchoixposte = pd.DataFrame({'Pos':["DF","MF","FW","GK","ALL"]})


pos = st.selectbox("Choix du poste a afficher pour strasbourg:",dfchoixposte['Pos'].unique(),index=None)


if pos == "FW" or pos == "DF" or pos == "MF":
    dfposte = dfrcsa2[(dfrcsa2['Unnamed: 2_level_0','Pos'].str.contains(pos)) & (dfrcsa2['Playing Time','Min']>90)]
    goals = dfposte['Performance']['Gls']
    xG = dfposte['Expected']['xG']
    playername = dfposte['Unnamed: 0_level_0','Player']

    # plot
    fig, ax = plt.subplots(figsize=(10,10))

    # Scatter plot
    sc2 = ax.scatter(xG, goals, color='grey')  # use a neutral color for points

    # Calculate mean values
    moyennegoals = goals.mean()
    moyennexG = xG.mean()

    x3_line = np.linspace(min(xG.min(), goals.min()), max(xG.max(), goals.max()), 100)
    ax.plot(x3_line, x3_line, label='y = x', color='black')  # Line plot y=x

    # Add mean lines
    ax.axvline(x=moyennexG, color='red', linestyle='--')  # Vertical line at mean xG
    ax.axhline(y=moyennegoals, color='blue', linestyle='--')  # Horizontal line at mean xGA

    # Annotate each point
    for i, txt in enumerate(playername):
        ax.annotate(txt, (xG.iloc[i], goals.iloc[i]))

    # Set labels and legend
    ax.set_xlabel('xG')
    ax.set_ylabel('Goals')
    ax.legend(['y = x', 'Mean xG', 'Mean xGA'], loc='upper left')

    st.pyplot(fig)
elif pos == "ALL" :
    dfposte = dfrcsa2[dfrcsa2['Playing Time','Min']>90]
    goals = dfposte['Performance']['Gls']
    xG = dfposte['Expected']['xG']
    playername = dfposte['Unnamed: 0_level_0','Player']

    # plot
    fig, ax = plt.subplots(figsize=(10,10))

    # Scatter plot
    sc2 = ax.scatter(xG, goals, color='grey')  # use a neutral color for points

    # Calculate mean values
    moyennegoals = goals.mean()
    moyennexG = xG.mean()

    x3_line = np.linspace(min(xG.min(), goals.min()), max(xG.max(), goals.max()), 100)
    ax.plot(x3_line, x3_line, label='y = x', color='black')  # Line plot y=x

    # Add mean lines
    ax.axvline(x=moyennexG, color='red', linestyle='--')  # Vertical line at mean xG
    ax.axhline(y=moyennegoals, color='blue', linestyle='--')  # Horizontal line at mean xGA

    # Annotate each point
    for i, txt in enumerate(playername):
        ax.annotate(txt, (xG.iloc[i], goals.iloc[i]))

    # Set labels and legend
    ax.set_xlabel('xG')
    ax.set_ylabel('Goals')
    ax.legend(['y = x', 'Mean xG', 'Mean xGA'], loc='upper left')

    st.pyplot(fig)





def xG_goals_per_player(df_input,input_poste):
    if input_poste == "FW" or input_poste == "DF" or input_poste == "MF":
        dfposte = df_input[(df_input['Unnamed: 2_level_0','Pos'].str.contains(input_poste)) & (df_input['Playing Time','Min']>90)]
        goals = dfposte['Performance']['Gls']
        xG = dfposte['Expected']['xG']
        playername = dfposte['Unnamed: 0_level_0','Player']

        # plot
        fig, ax = plt.subplots(figsize=(10,10))

        # Scatter plot
        sc2 = ax.scatter(xG, goals, color='grey')  # use a neutral color for points

        # Calculate mean values
        moyennegoals = goals.mean()
        moyennexG = xG.mean()

        x3_line = np.linspace(min(xG.min(), goals.min()), max(xG.max(), goals.max()), 100)
        ax.plot(x3_line, x3_line, label='y = x', color='black')  # Line plot y=x

        # Add mean lines
        ax.axvline(x=moyennexG, color='red', linestyle='--')  # Vertical line at mean xG
        ax.axhline(y=moyennegoals, color='blue', linestyle='--')  # Horizontal line at mean xGA

        # Annotate each point
        for i, txt in enumerate(playername):
            ax.annotate(txt, (xG.iloc[i], goals.iloc[i]))

        # Set labels and legend
        ax.set_xlabel('xG')
        ax.set_ylabel('Goals')
        ax.legend(['y = x', 'Mean xG', 'Mean xGA'], loc='upper left')

        st.pyplot(fig)

    elif input_poste == "ALL" :
        dfposte = df_input[df_input['Playing Time','Min']>90]
        goals= dfposte['Performance']['Gls']
        xG = dfposte['Expected']['xG']
        playername = dfposte['Unnamed: 0_level_0','Player']

        # plot
        fig, ax = plt.subplots(figsize=(10,10))

        # Scatter plot
        sc2 = ax.scatter(xG, goals, color='grey')  # use a neutral color for points

        # Calculate mean values
        moyennegoals = goals.mean()
        moyennexG= xG.mean()

        x3_line = np.linspace(min(xG.min(), goals.min()), max(xG.max(), goals.max()), 100)
        ax.plot(x3_line, x3_line, label='y = x', color='black')  # Line plot y=x

        # Add mean lines
        ax.axvline(x=moyennexG, color='red', linestyle='--')  # Vertical line at mean xG
        ax.axhline(y=moyennegoals, color='blue', linestyle='--')  # Horizontal line at mean xGA

        # Annotate each point
        for i, txt in enumerate(playername):
            ax.annotate(txt, (xG.iloc[i], goals.iloc[i]))

        # Set labels and legend
        ax.set_xlabel('xG')
        ax.set_ylabel('Goals')
        ax.legend(['y = x', 'Mean xG', 'Mean xGA'], loc='upper left')

        st.pyplot(fig)

def xG_goals_per_player_filtered_by_agee(df_input, input_poste, df_input_age):
    if input_poste in ["FW", "DF", "MF"]:
        dfposte = df_input[
            (df_input['Unnamed: 2_level_0', 'Pos'].str.contains(input_poste)) &
            (df_input['Playing Time', 'Min'] > 90) &
            (df_input['Unnamed: 3_level_0', 'Age'] < df_input_age)
        ]
    else:
        dfposte = df_input[df_input['Playing Time', 'Min'] > 90]

    goals = dfposte['Performance', 'Gls']
    xG = dfposte['Expected', 'xG']
    playername = dfposte['Unnamed: 0_level_0', 'Player']
    teamnames = dfposte['teamname']

    # Création du graphique
    fig, ax = plt.subplots(figsize=(10, 10))

    # Tracer la ligne y = x
    x3_line = np.linspace(min(xG.min(), goals.min()), max(xG.max(), goals.max()), 100)
    ax.plot(x3_line, x3_line, label='y = x', color='black')

    # Moyennes
    moyennegoals = goals.mean()
    moyennexG = xG.mean()
    ax.axvline(x=moyennexG, color='red', linestyle='--')
    ax.axhline(y=moyennegoals, color='blue', linestyle='--')

    # Affichage des logos sur le graphique
    plot_with_logos_andplayernames(xG, goals, teamnames,playername, ax)

    # Étiquettes et légende
    ax.set_xlabel('xG')
    ax.set_ylabel('Goals')
    ax.legend(['y = x', 'Mean xG', 'Mean xGA'], loc='upper left')

    st.pyplot(fig)

st.write("""
# Choose the pos and the age under to show the graph
""")

pos_all_ligue1_player= st.selectbox("Choix du poste a afficher :",dfchoixposte['Pos'].unique(),index=None)
age_under = st.selectbox("Age des joueurs inferieur a (default all) :",df_all_player_ligue1[('Unnamed: 3_level_0', 'Age')].sort_values().unique(),index=None)


if age_under == None:
    xG_goals_per_player_filtered_by_agee(df_all_player_ligue1,pos_all_ligue1_player,df_all_player_ligue1[('Unnamed: 3_level_0', 'Age')].max())
else:
    xG_goals_per_player_filtered_by_agee(df_all_player_ligue1,pos_all_ligue1_player,age_under)

print(df_all_player_ligue1)