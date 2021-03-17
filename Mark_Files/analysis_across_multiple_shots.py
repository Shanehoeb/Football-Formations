from functions import *

file = 'Data/7430.json'
f = open(file)
loaded_file = json.load(f)

shots = get_specific_events(loaded_file, 'Shot')
shot_start, shot_end = get_locations(shots)
expected_goals = get_xg(shots)

defence = defender_locations(shots)

post_1 = [120, 43.66]
post_2 = [120, 36.34]

defenders_in_way_array = []
xg_array = []
nearby_defenders_avg_dist_array = []
angle_array = []
distance_array = []

for i in range(np.shape(shot_start)[0]):

    x = shot_start[i]
    y = shot_end[i]

    dist = dist_between(y, x)

    angle_between_posts = [angle_between(x, post_1), angle_between(x, post_2)]

    angle_to_goal = np.mean(angle_between_posts)

    defenders = defence[i]

    nearby_defenders = closest_defenders(x, defenders, 3)

    avg_distance_from_nearby_defenders = avg_distance_from_defender(x, nearby_defenders)

    xg = expected_goals[i]

    defenders_in_way = which_defenders_in_front_of_goal(x, defenders, angle_between_posts)

    dist_over_angle = dist/abs(angle_to_goal)

    defenders_in_way_array.append(np.shape(defenders_in_way)[0])
    xg_array.append(xg)
    nearby_defenders_avg_dist_array.append(avg_distance_from_nearby_defenders)
    angle_array.append(abs(angle_to_goal))
    distance_array.append((dist_over_angle * np.shape(defenders_in_way)[0])/avg_distance_from_nearby_defenders)

plt.scatter(distance_array, xg_array)
plt.xlabel('Distance/Angle x Number of defenders in the way/Avg Distance from Nearby Defenders')
plt.ylabel('Expected Goals from Shot')
plt.show()
