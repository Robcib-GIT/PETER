clear; clc; close all;


if exist('ser','var')
    try
        clear ser
    catch
    end
end

com_port = "COM7";
baud = 115200;
ser = serialport(com_port, baud);
pause(2);

Kp = 60;   % select between 10-60
max_iter = 30;
err_h_tol = 0.5;
err_pos_norm_tol = 0.7;

total_duration=0;

desired_x = 3;
desired_y = 0;
desired_h = 67;

% Safety
write_one_valve_millis(ser, 1, -5000);
write_one_valve_millis(ser, 2, -5000);
write_one_valve_millis(ser, 3, -5000);
disp("Deflating valves...");
pause(5);

try
    disp('Reading initial IMU & TOF...');
    [~, pitch0, roll0, h0] = read_sensors(ser, true);

    measured_pitch = pitch0;
    measured_roll  = roll0;
    measured_h     = h0;

    [desired_pitch, desired_roll, desired_hh] = xyh_to_prh(desired_x, desired_y, desired_h);

    [hA_des, hB_des, hC_des] = prh_to_leg_heights(desired_pitch, desired_roll, desired_hh);

    for k = 1:max_iter
        [hA_meas, hB_meas, hC_meas] = prh_to_leg_heights(measured_pitch, measured_roll, measured_h);

        err_A = hA_des - hA_meas;
        err_B = hB_des - hB_meas;
        err_C = hC_des - hC_meas;

        tA = Kp * err_A;
        tB = Kp * err_B;
        tC = Kp * err_C;

        % VERY IMPORTANT
        % 1-C 3-B 2-A !!!!!
        write_one_valve_millis(ser, 1, tC);
        write_one_valve_millis(ser, 2, tA);
        write_one_valve_millis(ser, 3, tB);

        pause_duration = max([200, abs(tA), abs(tB), abs(tC)]) / 1000; % saniyeye çevir
        total_duration = total_duration + pause_duration;
        pause(pause_duration);

        [~, pitch_new, roll_new, h_new] = read_sensors_filtered(ser, true);
        measured_pitch = pitch_new;
        measured_roll  = roll_new;
        measured_h     = h_new;

        [x_c, y_c, h_c] = prh_to_xyh(measured_pitch, measured_roll, measured_h);

        pos_error = [desired_x - x_c, desired_y - y_c, desired_h - h_c];
        pos_norm = norm(pos_error(1:2));

        [hA_meas, hB_meas, hC_meas] = prh_to_leg_heights(measured_pitch, measured_roll, measured_h);

        fprintf('\n[Step %d]\n', k);
        fprintf('Valve times (ms):       [%.2f %.2f %.2f]\n', tA, tB, tC);
        fprintf('Desired Leg Heights:    [%.2f %.2f %.2f]\n', hA_des, hB_des, hC_des);
        fprintf('Current Leg Heights:    [%.2f %.2f %.2f]\n', hA_meas, hB_meas, hC_meas);
        fprintf('Desired PRH:            [%.2f %.2f %.2f]\n', desired_pitch, desired_roll, desired_h);
        fprintf('Current PRH:            [%.2f %.2f %.2f]\n', measured_pitch, measured_roll, measured_h);
        fprintf('Current Position:       [%.2f %.2f %.2f]\n', x_c, y_c, h_c);
        fprintf('Position error:         [%.2f %.2f] (norm=%.2f)\n', pos_error(1), pos_error(2), pos_norm);
        fprintf('H error: [%.2f]\n', pos_error(3));
        fprintf('Total_duration: [%.2f]\n',total_duration);

        if abs(pos_norm) < err_pos_norm_tol && abs(pos_error(3)) < err_h_tol
            disp('All leg errors below threshold. Converged.');
            break
        end
    end
catch ME
    
    disp(getReport(ME));
end


if exist('ser','var')
    try
        clear ser
    catch
    end
end
