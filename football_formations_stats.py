from football_formations import *
import pandas as pd
import glob
import codecs
import json

df = pd.DataFrame(columns=['HomeGoals', 'HomeFormation', 'AwayGoals', 'AwayFormation', 'Result'])

for file in glob.glob('open-data-master (1)/open-data-master/data/events/*.json'):
    with codecs.open(file, 'r', 'utf-8') as f:
        loaded_file = json.load(f, encoding='utf-b')

    home_formation = formation(loaded_file[0])
    away_formation = formation(loaded_file[1])

    home_goals, away_goals, result = get_score(loaded_file)
    data = [home_goals, home_formation, away_goals, away_formation, result]
    DataFrame = pd.DataFrame([data], columns=['HomeGoals', 'HomeFormation', 'AwayGoals', 'AwayFormation', 'Result'])
    df = pd.concat([df, DataFrame], ignore_index=True)


df.to_csv('Statsbomb_scores.csv')

