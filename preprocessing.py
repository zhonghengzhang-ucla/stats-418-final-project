import pandas as pd
import numpy as np

df = pd.read_csv('outfield_players.csv')
df = pd.concat([df, df['Position(s)'].str.replace(' ', '').str.get_dummies(sep=',')], axis=1)
df['Remaining PA'] = df['PA'] - df['CA']
df['Contract Expiring'] = df['Contract expiration (year)'] <= 1
df = df.dropna(subset=['Sell value (€)', 'Rel. clause (€)'], how='all')
df['Minimum Price'] = df[['Sell value (€)', 'Rel. clause (€)']].min(axis=1)
df = df.drop(columns=['Position(s)', 'UID', 'Height (CM)', 'Weight (KG)', 'International Caps', 'International Goals',
                      'Foot'])
df.to_csv('players.csv', index=False)