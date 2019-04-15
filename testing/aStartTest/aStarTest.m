% NAME: AstarTest.m
% AUTH: Ryan McCartney
% DATE: 15/04/2018
% DESC: Implementation of an A* Algorithm

% Some MATlab initialisation to clear Workspace and Command Window
clear;
clc;

width = 15;
height = 15;

initialPosition = [2,2];
goalPosition = [12,12];

%Generate Empty Map
R = zeros(width,height)+255;
G = zeros(width,height)+255;
B = zeros(width,height)+255;

%Generate Obstacles
ObstacleNumber = round(0.3*width*height);
ObstaclePositions = randperm(width*height,ObstacleNumber);

%Add Obstacle to Empty Map
R(ObstaclePositions) = 255;
G(ObstaclePositions) = 0;
B(ObstaclePositions) = 0;

%Concatenate Colour Channels
Map = cat(3,R,G,B);
Map(initialPosition(1),initialPosition(2),:) = [255,255,255];
Map(goalPosition(1),goalPosition(2),:) = [255,255,255];

%Show the Map with large scalling
figure(1);
clf();
imshow(Map);
truesize([300 300]);
hold on;
plot(initialPosition(1),initialPosition(2), 'g*', 'LineWidth', 2, 'MarkerSize', 15, 'DisplayName','Initial Position');
plot(goalPosition(1),goalPosition(2), 'b*', 'LineWidth', 2, 'MarkerSize', 15, 'DisplayName','Goal Position');
xlabel('Width')
ylabel('Height')
title('Randomly Generated Map for Solving');
legend;   

OpenList = [];
ClosedList = [];
currentPosition = initialPosition;
paths = [[0,1];[0,-1];[1,0];[-1,0]];

%Add Initial Position to Closed List
Map(initialPosition(1),initialPosition(2),:) = [0,0,255];
ClosedList = [initialPosition(1),initialPosition(2),0];

iterations = 1;
while isequal(currentPosition,goalPosition) == 0
    PathScore = 0;
    for i=1:4
        %Determine Path to Check
        adjacentPath = currentPosition+paths(i,:);
        pixelValue = impixel(Map,adjacentPath(2),adjacentPath(1));
        if pixelValue == [255,0,0]
            %disp("Obstacle, not a valid path. Ignoring.")
        elseif pixelValue == [255,0,50]
            %disp("Open list, no need to calculate again.")
        elseif impixel(Map,adjacentPath(1),adjacentPath(2)) == [0,0,255]
            %disp("Closed List, need not check again.")
        elseif (adjacentPath(1) < 1) || (adjacentPath(2) < 1)
            %disp("Edge of Image has been reacehd, ignoring.")
        elseif pixelValue == [255,255,255]
            %Determine Path Score for this Path
            G = abs(adjacentPath(1)-initialPosition(1)) + abs(adjacentPath(2)-initialPosition(2));
            H = abs(adjacentPath(1)-goalPosition(1)) + abs(adjacentPath(2)-goalPosition(2));
            PathScore = G + H;
            
            %Add Point to Open List (Colour Pixel Purple)
            Map(adjacentPath(1),adjacentPath(2),:) = [255,0,50];
            OpenList = [OpenList;adjacentPath(1),adjacentPath(2),PathScore];
        end        
    end
    
    %Show the Updated Map
    figure(2);
    hold on;
    imshow(Map);
    truesize([300 300]);
    xlabel('Width');
    ylabel('Height');
    title('Progress');
    pause(.1);

    %Determine Lowest Scoring Path and next move
    PathScores = OpenList(:,3);
    [lowestPathScore,lowestScoringPath] = min(PathScores);
    currentPosition = OpenList(lowestScoringPath,[1:2]);
    %Add Selected Route to Closed List
    Map(currentPosition(1),currentPosition(2),:) = [0,0,255];
    ClosedList(iterations,:) = [currentPosition(1),currentPosition(2),lowestScoringPath];
    %Remove the point from the open list
    OpenList(lowestScoringPath,:) = [];
    %Determine How Many Loops Have Passed
    %disp(['Iteration number ',num2str(iterations),' complete.'])
    iterations = iterations + 1;
end

%Determine Length of Closed List
closedListItems =size(ClosedList,1);

currentPosition = goalPosition;
paths = [[-1,0];[0,-1];[0,1];[1,0]];
Map(goalPosition(1),goalPosition(2),:) = [0,255,0];

%Now To Determine the Shortest Path
while isequal(currentPosition,initialPosition) == 0
    PathScores = [];
    for i=1:4
        adjacentPath = currentPosition+paths(i,:);
        pixelValue = impixel(Map,adjacentPath(2),adjacentPath(1));
        if pixelValue == [0,0,255]          
            [row,col] = find(ismember(adjacentPath, ClosedList));
            PathScores = [PathScores; adjacentPath(1),adjacentPath(2),ClosedList(row(1),3)]; 
        end
    end
    %Determine Lowest Scoring Path and next move
    PathScore = PathScores(:,3);
    [lowestPathScore,lowestScoringPath] = min(PathScore);
    currentPosition = PathScores(lowestScoringPath,[1:2]);
    Map(currentPosition(1),currentPosition(2),:) = [0,255,0];
    %Update Plot
    imshow(Map);
    truesize([300 300]);    
end

%Show the Map with large scalling
figure(3);
clf();
imshow(Map);
truesize([300 300]);
hold on;
plot(initialPosition(1),initialPosition(2), 'r*', 'LineWidth', 2, 'MarkerSize', 15, 'DisplayName','Initial Position');
plot(goalPosition(1),goalPosition(2), 'b*', 'LineWidth', 2, 'MarkerSize', 15, 'DisplayName','Goal Position');
xlabel('Width')
ylabel('Height')
title('A* Route Through Map');
legend;   

