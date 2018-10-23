%% Matrices and variables init
r = 180/pi; 
c = 340.29;
% Nominal position
NomP = [0, 6];
s0 = [-6, 0]; s1 = [0, 0]; s2 = [6, 0];

NomDist = [sqrt((s0(1)-NomP(1))^2+(s0(2)-NomP(2))^2),
        sqrt((s1(1)-NomP(1))^2+(s1(2)-NomP(2))^2), 
        sqrt((s2(1)-NomP(1))^2+(s2(2)-NomP(2))^2)];

NomAlpha = [r*acos(-6/NomDist(1)),
            r*acos(0/NomDist(2)), 
            r*acos(6/NomDist(3))];

            
% Covariance matrix C
A = [[-1, 1, 0];[0, -1, 1];];
C = A*A';

% Coefficient matrix H
H=(1/c)*[[cos(NomAlpha(2))-cos(NomAlpha(1)), sin(NomAlpha(2))-sin(NomAlpha(1))];
         [cos(NomAlpha(3))-cos(NomAlpha(2)), sin(NomAlpha(3))-sin(NomAlpha(2))]];

%% First  measures
m0 = sqrt((s0(1)-3)^2+(s0(2)-5)^2);  m1 = sqrt((s1(1)-3)^2+(s1(2)-5)^2);  m2 = sqrt((s2(1)-3)^2+(s2(2)-5)^2);
measure1 = (1/c)*[m0, m1, m2];
% TDOA measure
measure = [measure1(2)-measure1(1), measure1(3)-measure1(2)]';


%% BLUE estimator
theta = inv(H'*inv(C)*H)*(H'*inv(C)*measure)