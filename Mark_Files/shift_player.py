from functions import *

file = 'events/19728.json'
f = open(file)
loaded_file = json.load(f)

teams = get_teams(loaded_file)

lineup1 = get_lineup_arrays(loaded_file[0])
lineup2 = get_lineup_arrays(loaded_file[1])

player_ids_1 = get_line_up_with_player_id(loaded_file[0])
player_ids_2 = get_line_up_with_player_id(loaded_file[1])

print(player_ids_1)
