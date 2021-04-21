import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

path = 'Statsbomb_scores.csv'
df = pd.read_csv(path)
formation = 4231


def formation_data(df, formation, home_or_away, result):
    condition = df[(df[str(home_or_away) + "Formation"] == formation) & (df["Result"] == result)]

    if home_or_away == 'Home':
        return condition["AwayFormation"].tolist()
    else:
        return condition["HomeFormation"].tolist()


opposition_formation_home_w = formation_data(df, formation, 'Home', 'Home Win')
opposition_formation_home_l = formation_data(df, formation, 'Home', 'Away Win')
opposition_formation_home_d = formation_data(df, formation, 'Home', 'Draw')

opposition_formation_away_w = formation_data(df, formation, 'Away', 'Away Win')
opposition_formation_away_l = formation_data(df, formation, 'Away', 'Home Win')
opposition_formation_away_d = formation_data(df, formation, 'Away', 'Draw')

count_formations_home_w = dict(Counter(opposition_formation_home_w))
count_formations_home_l = dict(Counter(opposition_formation_home_l))
count_formations_home_d = dict(Counter(opposition_formation_home_d))

count_formations_away_w = dict(Counter(opposition_formation_away_w))
count_formations_away_l = dict(Counter(opposition_formation_away_l))
count_formations_away_d = dict(Counter(opposition_formation_away_d))

home_merge = dict(Counter(count_formations_home_w) + Counter(count_formations_home_l) + Counter(count_formations_home_d))
home_merge_win_percentage = {k: (count_formations_home_w[k] / home_merge[k]) for k in count_formations_home_w}
print('Opposition Formation Win Percentage (H):', home_merge_win_percentage)
home_merge_loss_percentage = {k: (count_formations_home_l[k] / home_merge[k]) for k in count_formations_home_l}
print('Opposition Formation Loss Percentage (H):', home_merge_loss_percentage)
home_merge_draw_percentage = {k: (count_formations_home_d[k] / home_merge[k]) for k in count_formations_home_d}
print('Opposition Formation Draw Percentage (H):', home_merge_draw_percentage)

away_merge = dict(Counter(count_formations_away_w) + Counter(count_formations_away_l) + Counter(count_formations_away_d))
away_merge_win_percentage = {k: (count_formations_away_w[k] / away_merge[k]) for k in count_formations_away_w}
print('Opposition Formation Win Percentage (A):', away_merge_win_percentage)
away_merge_loss_percentage = {k: (count_formations_away_l[k] / away_merge[k]) for k in count_formations_away_l}
print('Opposition Formation Loss Percentage (A):', away_merge_loss_percentage)
away_merge_draw_percentage = {k: (count_formations_away_d[k] / away_merge[k]) for k in count_formations_away_d}
print('Opposition Formation Draw Percentage (A):', away_merge_draw_percentage)

keys_values_home_w = home_merge_win_percentage.items()
home_win_percentage = {str(key): value for key, value in keys_values_home_w}
keys_values_home_l = home_merge_loss_percentage.items()
home_loss_percentage = {str(key): value for key, value in keys_values_home_l}
keys_values_home_d = home_merge_draw_percentage.items()
home_draw_percentage = {str(key): value for key, value in keys_values_home_d}

x = home_win_percentage.keys()
y = home_win_percentage.values()
plt.scatter(x,y, c='green', label='Win')
x = home_loss_percentage.keys()
y = home_loss_percentage.values()
plt.scatter(x,y, c='red', label='Loss')
x = home_draw_percentage.keys()
y = home_draw_percentage.values()
plt.scatter(x,y, c='blue', label='Draw')
plt.xlabel("Opposition Formation")
plt.ylabel("Win, Lose & Draw Percentage")
plt.title("Playing " + str(formation) + " at Home")
plt.legend()
plt.show()

keys_values_away_w = away_merge_win_percentage.items()
away_win_percentage = {str(key): value for key, value in keys_values_away_w}
keys_values_away_l = home_merge_loss_percentage.items()
away_loss_percentage = {str(key): value for key, value in keys_values_away_l}
keys_values_away_d = home_merge_draw_percentage.items()
away_draw_percentage = {str(key): value for key, value in keys_values_away_d}

x = away_win_percentage.keys()
y = away_win_percentage.values()
plt.scatter(x,y, c='green', label='Win')
x = away_loss_percentage.keys()
y = away_loss_percentage.values()
plt.scatter(x,y, c='red', label='Loss')
x = away_draw_percentage.keys()
y = away_draw_percentage.values()
plt.scatter(x,y, c='blue', label='Draw')
plt.xlabel("Opposition Formation")
plt.ylabel("Win, Lose & Draw Percentage")
plt.title("Playing " + str(formation) + " Away")
plt.legend()
plt.show()

''''
FINDING MODE

mode_formation_home_w = max(set(opposition_formation_home_w), key=opposition_formation_home_w.count)
mode_formation_home_l = max(set(opposition_formation_home_l), key=opposition_formation_home_l.count)
mode_formation_home_d = max(set(opposition_formation_home_d), key=opposition_formation_home_d.count)

mode_formation_away_w = max(set(opposition_formation_away_w), key=opposition_formation_away_w.count)
mode_formation_away_l = max(set(opposition_formation_away_l), key=opposition_formation_away_l.count)
mode_formation_away_d = max(set(opposition_formation_away_d), key=opposition_formation_away_d.count)

print('Home Mode Formation Win against:', mode_formation_home_w)
print('Home Mode Formation Loss against:', mode_formation_home_l)
print('Home Mode Formation Draw against:', mode_formation_home_d)

print('Away Mode Formation Win against:', mode_formation_away_w)
print('Away Mode Formation Loss against:', mode_formation_away_l)
print('Away Mode Formation Draw against:', mode_formation_away_d)
'''