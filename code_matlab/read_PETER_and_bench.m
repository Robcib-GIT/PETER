addpath('functions');

max_it = 10000; % Maximum number of iterations
steps_desired = 700; % Number of desired steps

if exist('ser_PETER','var')
    try
        clear ser_PETER
    catch
    end
end

if exist('ser_bench','var')
    try
        clear ser_bench
    catch
    end
end


% Connect to PETER
com_port_PETER = "COM5";
baud_PETER = 115200;
ser_PETER = serialport(com_port_PETER, baud_PETER);
pause(2);

% Connect to syringe bench
com_port_bench = "COM9";
baud_bench = 115200;
ser_bench = serialport(com_port_bench, baud_bench);
pause(2);

% The loop finishes when letter q is pressed or after 10000 iterations
data = zeros(10,max_it);
num_it = 0;
% Starts the movement
writeline(ser_bench, 'a' + string(steps_desired));   
t0 = datetime('now');
while num_it < max_it
    if strcmp(get(gcf, 'CurrentKey'), 'q')
        break;
    end
    
    [x, y, z, h, x1, y1, z1, h1] = read_sensors_filtered(ser_PETER, false);
    steps = read_steps(ser_bench);

    t = datetime('now');
    data(:, num_it + 1) = [t-t0; steps; x; y; z; h; x1; y1; z1; h1];

    num_it = num_it + 1;
end

% Save the data in a csv with name the current date (hh mm and seconds) and
% '_measurements.csv'
currentTime = datestr(t0, 'HH_MM_SS');
csvFileName = strcat(currentTime, '_measurements.csv');
writematrix(data(:, 1:num_it), csvFileName);
