import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import streamlit as st

df = pd.read_csv('players.csv')
dataset = df.dropna(subset=['Sell value (€)'])

attribute_list = ['Corners', 'Crossing', 'Dribbling', 'Finishing', 'First Touch', 'Free Kick Taking',
                  'Heading', 'Long Shots', 'Long Throws', 'Marking', 'Passing', 'Penalty Taking', 'Tackling',
                  'Technique', 'Aggression', 'Anticipation', 'Bravery', 'Composure', 'Concentration', 'Decisions'
                  'Determination', 'Flair', 'Leadership', 'Off the Ball', 'Positioning', 'Teamwork', 'Vision',
                  'Work Rate', 'Acceleration', 'Agility', 'Balance', 'Jumping Reach', 'Natural Fitness','Pace',
                  'Stamina', 'Strength']

X = dataset[attribute_list + ['Age', 'Remaining PA', 'Contract Expiring']]
y = dataset['Sell value (€)']

rf = RandomForestRegressor(n_estimators=100, random_state=418)
rf.fit(X, y)

st.sidebar.header('Filter')

age = st.sidebar.slider('Age', 15, 50)
position = st.sidebar.selectbox('Position',
                                ('DC', 'DL', 'DR', 'DM', 'WBL', 'WBR', 'MC', 'ML', 'MR', 'AMC', 'AML', 'AMR', 'ST'))
expiring_contract = st.sidebar.checkbox('Contract Expiring')

technicals = st.sidebar.multiselect('Attributes', attribute_list)

technical_range = {}
for attribute in technicals:
    if attribute in technicals:
        technical_range[attribute] = st.sidebar.slider(attribute, 1, 20, [15, 20])
    else:
        technical_range[attribute] = [1, 20]

