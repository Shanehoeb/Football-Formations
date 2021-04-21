import json
import numpy as np


class player:
  def __init__(self, name, id, x_loc, y_loc, team):
    self.name = name
    self.id = id
    self.xloc = x_loc
    self.yloc = y_loc
    self.team = team


def get_freezeframe(event, team1, team2):
    shot_team = event['team']['name']
    freeze_frame = event['shot']['freeze_frame']
    team_mates = []
    opponents = []
    shooter_name = event['player']['name']
    shooter_id = event['player']['id']
    shooter_location = event['location']
    team_mates.append(player(shooter_name, shooter_id, shooter_location[0], shooter_location[1], shot_team))
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
    return team_mates, opponents
