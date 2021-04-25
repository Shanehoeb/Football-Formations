#The pitch dimensions from original full size screen are [145:1035,282:1640]

#Scale like metrica sports data,  where (0.5,0.5) is kickoff
# Our pitch coordinates : 0 to 1358 in length, 0 to 890 in width
def scaler_x(detection):
    return detection/1358

def scaler_y(detection):
    return 1-(detection/890)


