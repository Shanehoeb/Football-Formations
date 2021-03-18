import numpy as np
import matplotlib.pyplot as plt
import json
import math


'''This gets the names of both the teams, as there is a dict at the start of the
game that has all of the game info'''
def get_teams(data):
    teams = []
    for i in range(np.size(data)):
        data_points = data[i]
        team_data = data_points['team']
        team_name = team_data['name']
        if team_name not in teams:
            teams.append(team_name)
    return teams


'''In this game info array, there is an array that has all of the players in
the team and the formation that the team are playing. From this, we can make
an accurate lineup for each team (shown by final line of func)'''
def get_lineup_arrays(team):
    tactics = team['tactics']
    formation = tactics['formation']
    formation = [int(x) for x in str(formation)]
    lineup_array = tactics['lineup']
    goalkeeper = lineup_array[0]['player']['name']
    lineup = [[(goalkeeper, 1)]]
    # adding the goalkeeper
    rows_added = 1
    while rows_added < len(formation)+1:
        players_added = 0
        for list in lineup:
            players_added += len(list)
        next_row = []
        for j in range(players_added, players_added + formation[rows_added-1]):
            next_row.append((lineup_array[j]['player']['name'], lineup_array[j]['position']['id']))
        rows_added += 1
        lineup.append(next_row)
    return lineup


def get_line_up_with_player_id(team):
    line_up_with_player_id = []
    tactics = team['tactics']
    lineup_array = tactics['lineup']
    for j in range(len(lineup_array)):
        line_up_with_player_id.append((lineup_array[j]['player']['name'], lineup_array[j]['player']['id']))
    return line_up_with_player_id


'''The event type parameter is a string of which event you want to isolate From
the rest of the data. e.g. 'shot' or 'pass' or 'tackle'. The function will
return an array of this specific event'''
def get_specific_events(data, event_type):
    array = []
    for i in range(np.size(data)):
        if data[i]['type']['name'] == event_type:
            array.append(data[i])
    return array


'''In every event, there is data for the location of the start of the event and
the end of the event. We can isolate these locations.'''
def get_locations(events_array):
    start = []
    end = []
    for i in range(np.size(events_array)):
        location = events_array[i]['location']
        end_location = events_array[i]['shot']['end_location']
        start.append(location)
        end.append([end_location[0], end_location[1]])
    return start, end


'''This follows the exact same code as the above function. If the event is a
shot then we get the array of all the expected goals for those shots'''
def get_xg(shots):
    xgs = []
    for i in range(np.size(shots)):
        xg = shots[i]['shot']['statsbomb_xg']
        xgs.append(xg)
    return xgs


'''Plotting 2D arrays was a pain so just created a func'''
def plot_2d_array(array, label):
    x_array = []
    y_array = []
    for i in range(np.shape(array)[0]):
        x = array[i][0]
        y = array[i][1]
        x_array.append(x)
        y_array.append(y)
    plt.scatter(x_array, y_array, label=label)
    return

'''The freeze frame shows the position of all other players on the pitch at the
time of the particular event. We can find the position of all defenders because
they will not have a 'teammate' label. And then we can find their locations'''
def defender_locations(events_array):
    locations_array = []
    for i in range(np.size(events_array)):
        freeze_frame = events_array[i]['shot']['freeze_frame']
        defend_locations = []
        for j in range(np.size(freeze_frame)):
            if not freeze_frame[j]['teammate']:
                defend_locations.append(freeze_frame[j]['location'])
        locations_array.append(defend_locations)
    return locations_array


'''Plots an arrow from the start of the shot to the end'''
def plot_arrows(array_1, array_2):
    for i in range(np.shape(array_1)[0]):
        x1 = array_1[i][0]
        x2 = array_2[i][0]
        y1 = array_1[i][1]
        y2 = array_2[i][1]
        plt.arrow(x1, y1, (x2 - x1), (y2 - y1), head_width=0.5, head_length=0.5, length_includes_head=True)
    return


def pitch_dimensions(all_events):
    min_length = 60
    max_length = 0
    max_width = 0
    min_width = 0
    key = 'location'
    for i in range(np.size(all_events)):
        if key in all_events[i]:
            location = all_events[i][key]
            if location[0] > max_length:
                max_length = location[0]
            if location[1] > max_width:
                max_width = location[1]
    length = [min_length, max_length]
    width = [min_width, max_width]
    return length, width


'''Self explanatory'''
def dist_between(point_1, point_2):
    distance = np.sqrt((point_2[0] - point_1[0]) ** 2 + (point_2[1] - point_1[1]) ** 2)
    return distance


'''Makes the graphs look sexy mate'''
def plot_pitch_markings():
    max_length = 120
    max_width = 80
    min_length = 90
    box_length = 16.5
    box_width = 40.3
    six_yard_length = 5.5
    six_yard_width = 18.32
    goal_length = 1
    goal_width = 7.32
    distance_from_touch_to_box = (max_width - box_width)/2
    distance_from_touch_to_six = (max_width - six_yard_width)/2
    distance_from_touch_to_goal = (max_width - goal_width)/2

    box_side_1 = np.linspace(120, 120-box_length, 1000)
    box_side_1_y = box_side_1*0 + distance_from_touch_to_box
    plt.plot(box_side_1, box_side_1_y, 'black')

    box_side_2_y = box_side_1*0 + (80 - distance_from_touch_to_box)
    plt.plot(box_side_1, box_side_2_y, 'black')

    box_side_width_y = np.linspace(distance_from_touch_to_box, (80 - distance_from_touch_to_box), 1000)
    box_side_width = box_side_width_y*0 + (120 - box_length)
    plt.plot(box_side_width, box_side_width_y, 'black')

    six_yard_side_1 = np.linspace(120, 120 - six_yard_length, 1000)
    six_yard_side_1_y = six_yard_side_1*0 + distance_from_touch_to_six
    plt.plot(six_yard_side_1, six_yard_side_1_y, 'black')

    six_yard_side_2_y = six_yard_side_1*0 + (80 - distance_from_touch_to_six)
    plt.plot(six_yard_side_1, six_yard_side_2_y, 'black')

    six_yard_box_width_y = np.linspace(distance_from_touch_to_six, (80 - distance_from_touch_to_six), 1000)
    six_yard_box_width = six_yard_box_width_y*0 + (120 - six_yard_length)
    plt.plot(six_yard_box_width, six_yard_box_width_y, 'black')

    pitch_width_plot_y = np.linspace(0, 80, 1000)
    pitch_width_plot = pitch_width_plot_y*0 + 120
    plt.plot(pitch_width_plot, pitch_width_plot_y, 'black')

    pitch_length_1 = np.linspace(min_length, max_length, 1000)
    pitch_length_1_y = pitch_length_1*0 + 0
    plt.plot(pitch_length_1, pitch_length_1_y, 'black')

    pitch_length_2_y = pitch_length_1*0 + max_width
    plt.plot(pitch_length_1, pitch_length_2_y, 'black')

    goal_length_1 = np.linspace(120, 120+goal_length, 1000)
    goal_length_1_y = goal_length_1*0 + distance_from_touch_to_goal
    plt.plot(goal_length_1, goal_length_1_y, 'black')

    goal_length_2_y = goal_length_1*0 + (max_width - distance_from_touch_to_goal)
    plt.plot(goal_length_1, goal_length_2_y, 'black')

    goal_width_plot_y = np.linspace(distance_from_touch_to_goal, (80 - distance_from_touch_to_goal), 1000)
    goal_width_plot = goal_width_plot_y*0 + (max_length + goal_length)
    plt.plot(goal_width_plot, goal_width_plot_y, 'black')
    return


'''This is used for when we works out the distances of the defenders away from
the attacker. We can then get the n number of smallest distances to work out
who the closest n defenders are.'''
def smallest_n_elements(array, n):
    smallest = []
    size_order = sorted(array)
    i = 0
    while i <= n - 1 and i < np.size(size_order):
        smallest.append(size_order[i])
        i += 1
    return smallest

'''Gets the closest n defenders from an array from a certain event.'''
def closest_defenders(shot_loc, defender_loc, no_of_defenders):
    distances = []
    for i in range(np.shape(defender_loc)[0]):
        distance = dist_between(defender_loc[i], shot_loc)
        distances.append(distance)
    smallest_distances = smallest_n_elements(distances, no_of_defenders)
    closest = []
    for distance in smallest_distances:
        for dist in distances:
            if distance == dist:
                index_of_small = distances.index(dist)
                closest.append(defender_loc[index_of_small])
                break
    return closest


'''The average dist from all of the defender distances'''
def avg_distance_from_defender(attacker, defenders):
    num_defenders = np.shape(defenders)[0]
    tot_distance = 0
    for i in range(num_defenders):
        distance_from_attacker = dist_between(defenders[i], attacker)
        tot_distance += distance_from_attacker
    mean_distance = tot_distance/num_defenders
    return mean_distance


'''Used to calculate the angle from the event to either post and also to work
out the angle between a defender and the shot'''
def angle_between(point_1, point_2):
    x_diff = point_2[0] - point_1[0]
    y_diff = point_2[1] - point_1[1]
    angle_between_points = 0
    if x_diff == 0:
        if y_diff > 0:
            angle_between_points = math.pi/2
        elif y_diff < 0:
            angle_between_points = -math.pi/2
    else:
        angle_between_points = math.atan(y_diff/x_diff)
    return angle_between_points


'''If we know the angle to both posts, and the angle from the shot to every
defender, then we can work out which defenders are in the way of the shot and
therefore most likely to block it (hence decreasing the likelihood of a goal)'''
def which_defenders_in_front_of_goal(striker, defenders, post_angles):
    blocking_defenders = []
    for i in range(np.shape(defenders)[0]):
        angle = angle_between(striker, defenders[i])
        if post_angles[1] < angle < post_angles[0] and defenders[i][0] > striker[0]:
            blocking_defenders.append(defenders[i])
    return blocking_defenders
