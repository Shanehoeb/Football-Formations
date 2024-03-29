import numpy as np
import matplotlib.pyplot as plt
import json
import math
import random


class player:
  def __init__(self, name, id, x_loc, y_loc, team):
    self.name = name
    self.id = id
    self.xloc = x_loc
    self.yloc = y_loc
    self.team = team
    
def get_score(loaded_file):
    home_goals = 0
    away_goals = 0

    shots = get_specific_events(loaded_file, 'Shot')
    teams = get_teams(loaded_file)

    for i in range(np.size(shots)):
        if shots[i]['shot']['outcome']['name'] == 'Goal':
            if shots[i]['team']['name'] == teams[0]:
                home_goals += 1
            else:
                away_goals += 1

    if home_goals == away_goals:
        result = 'Draw'
    elif home_goals > away_goals:
        result = 'Home Win'
    else:
        result = 'Away Win'
    return home_goals, away_goals, result


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
    lineup = [[(goalkeeper, lineup_array[0]['player']['id'])]]
    # adding the goalkeeper
    rows_added = 1
    while rows_added < len(formation)+1:
        players_added = 0
        for list in lineup:
            players_added += len(list)
        next_row = []
        for j in range(players_added, players_added + formation[rows_added-1]):
            next_row.append((lineup_array[j]['player']['name'], lineup_array[j]['player']['id']))
        rows_added += 1
        lineup.append(next_row)
    return lineup


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


def pitch_dimensions(all_events):
    min_length = 0
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
    min_length = 0
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

    box_side_1 = np.linspace(0, box_length, 1000)
    box_side_1_y = box_side_1*0 + distance_from_touch_to_box
    plt.plot(box_side_1, box_side_1_y, 'black')

    box_side_2_y = box_side_1*0 + (80 - distance_from_touch_to_box)
    plt.plot(box_side_1, box_side_2_y, 'black')

    box_side_width_y = np.linspace(distance_from_touch_to_box, (80 - distance_from_touch_to_box), 1000)
    box_side_width = box_side_width_y*0 + (box_length)
    plt.plot(box_side_width, box_side_width_y, 'black')

    six_yard_side_1 = np.linspace(0, six_yard_length, 1000)
    six_yard_side_1_y = six_yard_side_1*0 + distance_from_touch_to_six
    plt.plot(six_yard_side_1, six_yard_side_1_y, 'black')

    six_yard_side_2_y = six_yard_side_1*0 + (80 - distance_from_touch_to_six)
    plt.plot(six_yard_side_1, six_yard_side_2_y, 'black')

    six_yard_box_width_y = np.linspace(distance_from_touch_to_six, (80 - distance_from_touch_to_six), 1000)
    six_yard_box_width = six_yard_box_width_y*0 + (six_yard_length)
    plt.plot(six_yard_box_width, six_yard_box_width_y, 'black')

    pitch_width_plot_y = np.linspace(0, 80, 1000)
    pitch_width_plot = pitch_width_plot_y*0
    plt.plot(pitch_width_plot, pitch_width_plot_y, 'black')

    pitch_length_1 = np.linspace(min_length, max_length, 1000)
    pitch_length_1_y = pitch_length_1*0 + 0
    plt.plot(pitch_length_1, pitch_length_1_y, 'black')

    pitch_length_2_y = pitch_length_1*0 + max_width
    plt.plot(pitch_length_1, pitch_length_2_y, 'black')

    goal_length_1 = np.linspace(0, -goal_length, 1000)
    goal_length_1_y = goal_length_1*0 + distance_from_touch_to_goal
    plt.plot(goal_length_1, goal_length_1_y, 'black')

    goal_length_2_y = goal_length_1*0 + (max_width - distance_from_touch_to_goal)
    plt.plot(goal_length_1, goal_length_2_y, 'black')

    goal_width_plot_y = np.linspace(distance_from_touch_to_goal, (80 - distance_from_touch_to_goal), 1000)
    goal_width_plot = goal_width_plot_y*0 + (-goal_length)
    plt.plot(goal_width_plot, goal_width_plot_y, 'black')

    plt.plot(np.array([60, 60]), np.array([0, max_width]), 'black')

    return


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


'''Get a rough estimate of the initial positions of the players in the starting
XI'''
def initial_positions(lineup, pitch_dimensions, team_no, team_name):
    team_locations = []
    num_length_sections = len(lineup) - 1
    length_increments = np.mean(pitch_dimensions[0])/num_length_sections
    for i in range(len(lineup)):
        if team_no == 1:
            player_length = length_increments*i - 1
        elif team_no == 2:
            player_length = ((team_no-1)*pitch_dimensions[0][1]) - (length_increments*i - 1)
        num_width_sections = len(lineup[i])
        width_increments = np.max(pitch_dimensions[1])/num_width_sections
        sections = []
        for j in range(len(lineup[i])+1):
            sections.append(width_increments*j)
        for j in range(len(lineup[i])):
            player_width = np.mean([sections[j], sections[j+1]])
            team_locations.append(player(lineup[i][j][0], lineup[i][j][1], float(player_length), float(player_width), team_name))
    return np.asarray(team_locations)


'''Plot the current positions of the players on the pitch'''
def plot_team(team_1_loc, team_2_loc):
    for player in team_1_loc:
        plt.scatter(player.xloc, player.yloc, c='b', s=5)
    for player in team_2_loc:
        plt.scatter(player.xloc, player.yloc, c='r', s=5)
    plot_pitch_markings()
    return


'''Identify the player who was responsible for an event in a game'''
def identify_player(event, team_list):
    for team in team_list:
        for player in team:
            if player.id == event['player']['id']:
                return event['location'], player


def check_for_recipient(event, team_list):
    if event['type']['name'] == 'Pass':
        for team in team_list:
            for player in team:
                if player.id == event['pass']['recipient']['id']:
                    return event['pass']['end_location'], player
    else:
        return None, None


'''See if there has been a substitution before every event so that the list of
players can be updated'''
def check_sub(event, team_list):
    if event['type']['name'] != 'Substitution':
        return
    else:
        for team in team_list:
            for player in team:
                if player.id == event['player']['id']:
                    player.id = event['substitution']['replacement']['id']
                    player.name = event['substitution']['replacement']['name']
        return


def change_in_position(location, player):
    change_in_loc = np.array(location) - np.array([player.xloc, player.yloc])
    return change_in_loc


def change_all_locations(event, team_list, player_in_event, loc_change, pitch_dimensions):
    goalkeepers = [team_list[0][0], team_list[1][0]]
    check_sub(event, team_list)
    possible_distance = distance_possible_to_travel(event, 5)
    possession_team = which_team(event)
    if check_for_freeze_frame == True:
        team_list = convert_from_freeze_frame(event, team_list)
        return team_list
    if event['type']['name'] == 'Carry':
        player_in_event.xloc = event['carry']['end_location'][0]
        player_in_event.yloc = event['carry']['end_location'][1]
    elif event['type']['name'] == ['Pass']:
        recipient_location, recipient = check_for_recipient(event, team_list)
        recipient.xloc = recipient_location[0]
        recipient.yloc = recipient_location[1]
    else:
        player_in_event.xloc = event['location'][0]
        player_in_event.yloc = event['location'][1]
    if loc_change[0] == 0 and loc_change[1] == 0:
        return team_list
    else:
        for team in team_list:
            for player in team:
                if player not in goalkeepers:
                    location_change(pitch_dimensions, player, loc_change, possible_distance)
    return team_list


def check_for_freeze_frame(event):
    if event['type']['name'] == 'Shot':
        return True
    else:
        return False


def convert_from_freeze_frame(event, team_list):
    freeze_frame = event['shot']['freeze_frame']
    for i in range(np.shape(freeze_frame)[0]):
        for team in team_list:
            for player in team:
                if freeze_frame[i]['player']['name'] == player.name:
                    player.xloc = freeze_frame[i]['location'][0]
                    player.yloc = freeze_frame[i]['location'][1]
    return team_list



def location_change(pitch_dimensions, player, change_in_loc, distance):
    angle = math.atan(change_in_loc[1]/change_in_loc[0])
    i = 0
    while i != 1:
        player.xloc, player.yloc = change_loc(player.xloc, player.yloc, angle, distance)
        if is_on_pitch(player, pitch_dimensions) == True:
            i = 1
    return


def change_loc(x, y, angle, distance):
    movement_angle = random.uniform(-angle, angle)
    movement_distance = random.uniform(-distance, distance)
    x += movement_distance*math.cos(movement_angle)
    y += movement_distance*math.sin(movement_angle)
    return x, y


def location_change_defenders(pitch_dimensions, player, change_in_loc, distance):
    angle = math.atan(change_in_loc[1]/change_in_loc[0])
    i = 0
    while i != 1:
        movement_distance = random.uniform(0, -distance)
        player.xloc, player.yloc = change_loc(player.xloc, player.yloc, angle, distance)
        if is_on_pitch(player, pitch_dimensions):
            i = 1
    return


def is_on_pitch(player, pitch_dimensions):
    if pitch_dimensions[0][0] < player.xloc < pitch_dimensions[0][1]:
        if pitch_dimensions[1][0] < player.yloc < pitch_dimensions[1][1]:
            return True
        else:
            return False
    else:
        return False


def which_team(event):
    return event['possession_team']['name']


def distance_possible_to_travel(event, speed):
    if 'duration' in event:
        duration = event['duration']
    else:
        return 0
    possible_distance = speed*duration
    return possible_distance
