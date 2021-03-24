from functions import *

file = 'events/19728.json'
f = open(file)
loaded_file = json.load(f)

teams = get_teams(loaded_file)

lineup1 = get_lineup_arrays(loaded_file[0])
lineup2 = get_lineup_arrays(loaded_file[1])

dimensions = ([0, 120], [0, 80])

locations_1 = initial_positions(lineup1, dimensions, 1, teams[0])
locations_2 = initial_positions(lineup2, dimensions, 2, teams[1])
plot_team(locations_1, locations_2)

team_array = [locations_1, locations_2]
for moment_index in range(4, 15):
    #plot_team(team_array[0], team_array[1])
    loc, player = identify_player(loaded_file[moment_index], team_array)
    player_loc = [player.xloc, player.yloc]
    change_in_pos = change_in_position(loc, player)
    team_array = change_all_locations(loaded_file[moment_index], team_array, player, change_in_pos, dimensions)

#plot_team(change[0], change[1])
