from mplsoccer.pitch import Pitch
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation


# load away data from  https://github.com/metrica-sports/sample-data 
link1 = r"C:\Users\Shane\Desktop\Year 3\Mathematical and Data Modelling\Phase C\sample-data-master\data\Sample_Game_1\Sample_Game_1_RawTrackingData_Away_Team.csv"
df_away = pd.read_csv(link1, skiprows=2)
df_away.sort_values('Time [s]', inplace=True)

# load home data
link2 = r"C:\Users\Shane\Desktop\Year 3\Mathematical and Data Modelling\Phase C\sample-data-master\data\Sample_Game_1\Sample_Game_1_RawTrackingData_Home_Team.csv"
df_home = pd.read_csv(link2, skiprows=2)
df_home.sort_values('Time [s]', inplace=True)

# column names aren't great so this sets the player ones with _x and _y suffixes


def set_col_names(df):
    cols = list(np.repeat(df.columns[3::2], 2))
    cols = [col+'_x' if i % 2 == 0 else col+'_y' for i, col in enumerate(cols)]
    cols = np.concatenate([df.columns[:3], cols])
    df.columns = cols


set_col_names(df_away)
set_col_names(df_home)

lower_time = 0 #start of simulation in seconds
upper_time = 60 #end of simulation in seconds
fps = 25

df_away = df_away[(df_away['Time [s]'] >= lower_time*fps) & (df_away['Time [s]'] < upper_time*fps)].copy()
df_home = df_home[(df_home['Time [s]'] >= lower_time*fps) & (df_home['Time [s]'] < upper_time*fps)].copy()


# split off a df_ball dataframe and drop the ball columns from the player dataframes
df_ball = df_away[['Period', 'Frame', 'Time [s]', 'Ball_x', 'Ball_y']].copy()
df_home.drop(['Ball_x', 'Ball_y'], axis=1, inplace=True)
df_away.drop(['Ball_x', 'Ball_y'], axis=1, inplace=True)
df_ball.rename({'Ball_x': 'x', 'Ball_y': 'y'}, axis=1, inplace=True)


# convert to long form from wide form
def to_long_form(df):
    df = pd.melt(df, id_vars=df.columns[:3], value_vars=df.columns[3:], var_name='player')
    df.loc[df.player.str.contains('_x'), 'coordinate'] = 'x'
    df.loc[df.player.str.contains('_y'), 'coordinate'] = 'y'
    df = df.dropna(axis=0, how='any')
    df['player'] = df.player.str[6:-2]
    df = (df.set_index(['Period', 'Frame', 'Time [s]', 'player', 'coordinate'])['value']
          .unstack()
          .reset_index()
          .rename_axis(None, axis=1))
    return df


df_away = to_long_form(df_away)
df_home = to_long_form(df_home)


# First set up the figure, the axis
pitch = Pitch(pitch_type='metricasports', figsize=(16, 10.4),
              pitch_width=68, pitch_length=105, goal_type='line')
fig, ax = pitch.draw()

# then setup the pitch plot markers we want to animate
marker_kwargs = {'marker': 'o', 'markeredgecolor': 'black', 'linestyle': 'None'}
ball, = ax.plot([], [], ms=6, markerfacecolor='w', zorder=3, **marker_kwargs)
away, = ax.plot([], [], ms=10, markerfacecolor='#b94b75', **marker_kwargs)  # red/maroon
home, = ax.plot([], [], ms=10, markerfacecolor='#7f63b8', **marker_kwargs)  # purple


# animation function
def animate(i):
    # set the ball data with the x and y positions for the ith frame
    ball.set_data(df_ball.iloc[i, 3], df_ball.iloc[i, 4])
    # get the frame id for the ith frame
    frame = df_ball.iloc[i, 1]
    # set the player data using the frame id
    away.set_data(df_away.loc[df_away.Frame == frame, 'x'],
                  df_away.loc[df_away.Frame == frame, 'y'])
    home.set_data(df_home.loc[df_home.Frame == frame, 'x'],
                  df_home.loc[df_home.Frame == frame, 'y'])
    return ball, away, home


# call the animator, animate so 25 frames per second
anim = animation.FuncAnimation(fig, animate, frames=len(df_ball), interval=50, blit=True)
plt.show()
