from functions import *

file = 'C:/Users/crowl/PycharmProjects/xG/open-data-master/open-data-master/data/events/7445.json'
f = open(file)
loaded_file = json.load(f)

teams = get_teams(loaded_file)

lineups = [loaded_file[0], loaded_file[1]]

lineup_1 = get_lineup_arrays(lineups[0])
lineup_2 = get_lineup_arrays(lineups[1])
