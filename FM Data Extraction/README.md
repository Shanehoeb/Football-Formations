FM Data Extraction : Extracting player trajectories and event data from 2D FM Gameplay


Plan Outline  

1. Retrieve video clips of football manager gameplay
2. Use object detection algorithms to identify player positions and ball position for each frame of video clip
3. Use tracking algorithms to assign data to a player ID
4. Using ball and player positions to generate event data : code at https://github.com/vi3itor/soccer-event-recognition, paper at https://www.researchgate.net/publication/292995807_Recognizing_Compound_Events_in_Spatio-Temporal_Football_Data
5. Format data in same style as metrica
6. Use EPV/Pitch Control models on FM data to evaluate collective team movement


Files for each step 

1) FM_video_edit
2) circles.py and Mark&Josh functions
3) track.m and particle.m -- > Requires data in csv/excel format Frame_Number| x_coor | y_coor
4) Soccer event recognition --> requires input in pickle file, array of rows columns and 46 columns where the entries are the x-y positions of players at every frame
5) Scaler.py



