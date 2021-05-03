import pandas as pd
import numpy as np
import pickle

away_csv = pd.read_csv('sample-data-master/data/Sample_Game_1/Sample_Game_1_RawTrackingData_Away_Team.csv')
home_csv = pd.read_csv('sample-data-master/data/Sample_Game_1/Sample_Game_1_RawTrackingData_Home_Team.csv')

ball_x = home_csv['Ball_x']
ball_y = home_csv['Ball_y']

print(np.min(ball_x), np.max(ball_x))
print(np.min(ball_y), np.max(ball_y))

array_of_arrays = []
for i in range(0, 1425):
    array = []
    for j in range(1, 12):
        string_home_x = 'HPlayer' + str(j) + '_x'
        string_home_y = 'HPlayer' + str(j) + '_y'
        string_away_x = 'APlayer' + str(j) + '_x'
        string_away_y = 'APlayer' + str(j) + '_y'
        array.append(home_csv.iloc[i][string_home_x])
        array.append(home_csv.iloc[i][string_home_y])
        array.append(away_csv.iloc[i][string_away_x])
        array.append(away_csv.iloc[i][string_away_y])
    array.append(home_csv.iloc[i]['Ball_x'])
    array.append(home_csv.iloc[i]['Ball_y'])
    array_of_arrays.append(array)

array_of_arrays = np.asarray(array_of_arrays, dtype=np.float32)

print(np.shape(array_of_arrays))
dict = {'game': array_of_arrays}
print(dict)

with open('input/game_array.pkl', 'wb') as f:
    pickle.dump(dict, f)
