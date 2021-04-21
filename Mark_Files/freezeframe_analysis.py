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
            shot_team = loaded_file[i]['team']['name']
            freeze_frame = loaded_file[i]['shot']['freeze_frame']
            team_mates = []
            opponents = []
            for player_no in range(np.shape(freeze_frame)[0]):
                location = freeze_frame[player_no]['location']
                player_name = freeze_frame[player_no]['player']['name']
                player_id = freeze_frame[player_no]['player']['id']
                if freeze_frame[player_no]['teammate'] == True:
                    team = shot_team
                    team_mates.append(player(player_name, player_id, location[0], location[1], team))
                else:
                    if team1 == shot_team:
                        team = team2
                    else:
                        team = team1
                    opponents.append(player(player_name, player_id, location[0], location[1], team))
            print(team_mates)
            print(opponents)
            plot_team(team_mates, opponents)
            plt.show()
