import pandas as pd
import streamlit as st
import requests

st.sidebar.header('Filter')

attribute_dict = {}

add_age = st.sidebar.checkbox('Age')
if add_age:
    age = st.sidebar.slider('Age', 15, 50, [25, 30])
else:
    age = [15, 50]

position = st.sidebar.selectbox('Position',
                                ('DC', 'DL', 'DR', 'DM', 'WBL', 'WBR', 'MC', 'ML', 'MR', 'AMC', 'AML', 'AMR', 'ST'),
                                index=None)
expiring_contract = st.sidebar.checkbox('Contract Expiring')

attribute_list = ['Corners', 'Crossing', 'Dribbling', 'Finishing', 'First Touch', 'Free Kick Taking',
                  'Heading', 'Long Shots', 'Long Throws', 'Marking', 'Passing', 'Penalty Taking', 'Tackling',
                  'Technique', 'Aggression', 'Anticipation', 'Bravery', 'Composure', 'Concentration', 'Decisions',
                  'Determination', 'Flair', 'Leadership', 'Off the Ball', 'Positioning', 'Teamwork', 'Vision',
                  'Work Rate', 'Acceleration', 'Agility', 'Balance', 'Jumping Reach', 'Natural Fitness','Pace',
                  'Stamina', 'Strength']

attributes = st.sidebar.multiselect('Attributes', attribute_list)

for attribute in attribute_list:
    if attribute in attributes:
        attribute_dict[attribute] = st.sidebar.slider(attribute, 1, 20, [15, 20])
    else:
        attribute_dict[attribute] = [1, 20]

input_dict = {}
for attribute in attribute_dict:
    input_dict[attribute] = float(attribute_dict[attribute][0])
input_dict['Age'] = float(age[0])
input_dict['Contract Expiring'] = 1.0 if expiring_contract else 0.0

response = requests.post('https://stats-418-final-project-1088042122942.us-west1.run.app/pricer', json=input_dict, headers = {"content-type":"application/json"})
prediction = response.json()
predicted_price = list(prediction.values())[0]

players = pd.read_csv('players.csv')
player_selection = players
if position is not None:
    player_selection = player_selection.query(f'{position} == 1')
for attribute in attributes:
    player_selection = player_selection.query(f'`{attribute}` >= {attribute_dict[attribute][0]}')
    player_selection = player_selection.query(f'`{attribute}` <= {attribute_dict[attribute][1]}')
if add_age:
    player_selection = player_selection.query(f'Age >= {age[0]}')
    player_selection = player_selection.query(f'Age <= {age[1]}')
if expiring_contract:
    player_selection = player_selection.query('`Contract Expiring` == 1')

st.title('Football Manager 2023 Player Pricer & Recommender')
st.header('Projected Sell Value for Youngest Minimum Viable Player')
st.write(f'Predicted sell value: €{predicted_price[0]:,.0f}')

st.header('Recommended Players')
if player_selection.shape[0] == 0:
    st.write('No players found or available for purchase. Please adjust your filters.')
else:
    st.subheader('Best Player')
    best = player_selection.sort_values(['CA', 'Minimum Price', 'Age', 'Wages (€)'],
                                        ascending=[False, True, True, True]).iloc[0]
    st.write(f'Name: {best['Name']}')
    st.write(f'Club: {best['Club']}')
    st.write(f'Price: €{best['Minimum Price']:,.0f}')

    st.subheader('Cheapest Player')
    cheapest = player_selection.sort_values(['Minimum Price', 'CA', 'Age', 'Wages (€)'],
                                            ascending=[True, False, True, True]).iloc[0]
    st.write(f'Name: {cheapest['Name']}')
    st.write(f'Club: {cheapest['Club']}')
    st.write(f'Price: €{cheapest['Minimum Price']:,.0f}')

    st.subheader('Youngest Player')
    youngest = player_selection.sort_values(['Age', 'Minimum Price', 'CA', 'Wages (€)'],
                                            ascending=[True, True, False, True]).iloc[0]
    st.write(f'Name: {youngest['Name']}')
    st.write(f'Club: {youngest['Club']}')
    st.write(f'Price: €{youngest['Minimum Price']:,.0f}')
