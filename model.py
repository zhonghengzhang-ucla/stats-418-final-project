import pickle

import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor

df = pd.read_csv('players.csv')
dataset = df.dropna(subset=['Sell value (€)'])

x_variables = ['Corners', 'Crossing', 'Dribbling', 'Finishing', 'First Touch', 'Free Kick Taking', 'Heading',
               'Long Shots', 'Long Throws', 'Marking', 'Passing', 'Penalty Taking', 'Tackling', 'Technique',
               'Aggression', 'Anticipation', 'Bravery', 'Composure', 'Concentration', 'Decisions', 'Determination',
               'Flair', 'Leadership', 'Off the Ball', 'Positioning', 'Teamwork', 'Vision', 'Work Rate',
               'Acceleration', 'Agility', 'Balance', 'Jumping Reach', 'Natural Fitness', 'Pace', 'Stamina', 'Strength',
               'Age', 'Contract Expiring']

X = dataset[x_variables]
y = dataset['Sell value (€)']

model = HistGradientBoostingRegressor(random_state=418)
model.fit(X, y)

with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
