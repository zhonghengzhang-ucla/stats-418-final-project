import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor

df = pd.read_csv('players.csv')
dataset = df.dropna(subset=['Sell value (€)'])

predictors = ['Corners', 'Crossing', 'Dribbling', 'Finishing', 'First Touch', 'Free Kick Taking', 'Heading',
               'Long Shots', 'Long Throws', 'Marking', 'Passing', 'Penalty Taking', 'Tackling', 'Technique',
               'Aggression', 'Anticipation', 'Bravery', 'Composure', 'Concentration', 'Decisions', 'Determination',
               'Flair', 'Leadership', 'Off the Ball', 'Positioning', 'Teamwork', 'Vision', 'Work Rate',
               'Acceleration', 'Agility', 'Balance', 'Jumping Reach', 'Natural Fitness', 'Pace', 'Stamina', 'Strength',
               'Age', 'Contract Expiring']

model = HistGradientBoostingRegressor(random_state=418)
model.fit(dataset[predictors], dataset['Sell value (€)'])

def predict(input: dict) -> float:
    X = pd.DataFrame(input, index=[0], dtype=float)[predictors]
    y = model.predict(X)[0]
    return y