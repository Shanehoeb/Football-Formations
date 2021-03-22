from functions import *

file = 'events/19728.json'
f = open(file)
loaded_file = json.load(f)

teams = get_teams(loaded_file)

lineup1 = get_lineup_arrays(loaded_file[0])
lineup2 = get_lineup_arrays(loaded_file[1])

dimensions = ([0, 120], [0, 80])

initial_pos_1 = initial_positions(lineup1, dimensions, 1, teams[0])
initial_pos_2 = initial_positions(lineup2, dimensions, 2, teams[1])

change = [initial_pos_1, initial_pos_2]
for i in range(10, 20):
    change = change_all_locations(loaded_file[i], change)
    plot_team(change[0], change[1])
plt.show()


#for location in initial_pos:
