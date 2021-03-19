from functions import *

file = 'events/19728.json'
f = open(file)
loaded_file = json.load(f)

teams = get_teams(loaded_file)

lineup1 = get_lineup_arrays(loaded_file[0])
lineup2 = get_lineup_arrays(loaded_file[1])

dimensions = ([0, 120], [0, 80])

initial_pos_1 = initial_positions(lineup1, dimensions, 1)
initial_pos_2 = initial_positions(lineup2, dimensions, 2)

for i in range(np.size(loaded_file)):
    loc, player = identify_player(loaded_file[i], [initial_pos_1, initial_pos_2])
    print(player.name)

#plot_team(initial_pos_1, initial_pos_2)
#plt.show()


#for location in initial_pos:
