'''All of the functions become quite clear once looking at the data itself as
each game event is basically a huge dictionary so we have to go in each of the
dictionarys to access the data'''

from functions import *

file = 'Data/7430.json'
f = open(file)
loaded_file = json.load(f)

# We can isolate the game events that are shots (could be passes or interceptions)
shots = get_specific_events(loaded_file, 'Shot')
# Get the co-ordinates of the starting and ending location of all shots
shot_start, shot_end, expected_goals = get_locations(shots)
# Has the locations of the defenders when the shot is taken
defence = defender_locations(shots)

# Locations of both posts (We can see if a shot goes in)
post_1 = [120, 43.66]
post_2 = [120, 36.34]

# Isolating the positions for an individual shot (2nd in this case)
x = shot_start[2]
y = shot_end[2]

# Angle between the shot location and both of the posts
angle_between_posts = [angle_between(x, post_1), angle_between(x, post_2)]

# We then take an average of this to work out the angle to goal
angle_to_goal = np.mean(angle_between_posts)

# Getting the defender locations for that specific shot
defenders = defence[2]

# The statsbomb calculated expected goals for the shot
expected_goals = expected_goals[2]

# Getting the defenders that lie between the angle of the posts
defenders_in_way = which_defenders_in_front_of_goal(x, defenders, angle_between_posts)

# The closest defenders (shot_loc, defenders, how many defenders?)
nearby_defenders = closest_defenders(x, first_defenders, 4)
# Self explanatory
avg_distance_from_nearby_defenders = avg_distance_from_defender(x, nearby_defenders)

# Plotting the shot, the closest defenders and the defenders in the way of the shot
plt.scatter(x[0], x[1], label='Attacker')
plot_2d_array(defenders, 'other defenders')
plot_2d_array(defenders_in_way, 'defenders in way')
plot_pitch_markings()
plt.arrow(x[0], x[1], (y[0] - x[0]), (y[1] - x[1]), head_width=2, head_length=1, length_includes_head=True, color='r')
plt.title('Attacker and Defender locations for a shot with xG = ' + str(expected_goals))
plt.legend(loc='best')
plt.show()
