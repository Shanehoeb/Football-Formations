from freezeframe_funcs import *
from functions import *

file = 'events/19728.json'
f = open(file)
loaded_file = json.load(f)

teams = get_teams(loaded_file)
team1 = teams[0]
team2 = teams[1]

for i in range(np.size(loaded_file)):
    if loaded_file[i]['type']['name'] == 'Shot':
        if 'freeze_frame' in loaded_file[i]['shot']:
            attack, defence = get_freezeframe(loaded_file[i], team1, team2)
            print(attack)
            print(defence)
            plot_team(attack, defence)
            plt.show()
