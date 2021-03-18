from functions import *

file = 'events/19725.json'
f = open(file)
loaded_file = json.load(f)

teams = get_teams(loaded_file)

lineup1 = get_lineup_arrays(loaded_file[0])
lineup2 = get_lineup_arrays(loaded_file[1])

dimensions = ([0, 120], [0, 80])

initial_pos_1 = initial_positions(lineup1, dimensions, 1)
initial_pos_2 = initial_positions(lineup2, dimensions, 2)

for player in initial_pos_1:
    plt.scatter(player.xloc, player.yloc, c='b')

for player in initial_pos_2:
    plt.scatter(player.xloc, player.yloc, c='r')


plot_pitch_markings()
plt.ylim(0, 80)
plt.show()


#for location in initial_pos:
