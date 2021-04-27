clear;
%Load data from excel table where columns are | detection count | frame number | x center coordinate | y center cordinate |
%Format data
path = "C:\Users\Shane\Desktop\Year 3\Mathematical and Data Modelling\Phase B\mojo_sperm_tracking_data_bristol\mojo_sperm_tracking_data_bristol\tp49\cover0_4_YOLO_NO_TRACKING_output\vid_4_centers.xlsx"
vid0centers = readtable(path);
vid0centers.Var4 = vid0centers.Var4 *2 ;
vid0centers.Var3 = vid0centers.Var3 *2 ;
vid0centers.Var1 = [] ;
a = vid0centers.Var2(:);
vid0centers.Var2 = [] ;
vid0centers = vid0centers{:,:};
vid0centers(:,3) = a;

% Tracking parameters, see track.m
param.mem = 100;
param.dim = 2;
param.good = 1;
param.quiet = 0;




%max distance travelled in a time step
maxdisp = 200;

%Tracker
[tr ]=track(vid0centers,maxdisp,param);

%Plot results
hScatter = gscatter(tr(:,1),tr(:,2),tr(:,4));
for k = 1:numel(hScatter)
set(hScatter(k),'Color',rand(1,3))
end
