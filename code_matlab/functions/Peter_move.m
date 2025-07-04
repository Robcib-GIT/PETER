function PETER_move(com_port, desired_x, desired_y, desired_h, Kp)
% PETER_move moves the PETER robot platform to the desired (x, y, h) position
% using iterative closed-loop control.
%
% Arguments:
%   com_port: Serial port to connect (e.g., 'COM7')
%   desired_x: Target X coordinate (mm)
%   desired_y: Target Y coordinate (mm)
%   desired_h: Target height (mm)
%   Kp: Proportional gain for controller
%
% Example: PETER_move('COM7', 3, -2, 63, 60)

    % Fixed parameters
    max_iter = 20;           % Maximum number of iterations in each control loop
    err_h_tol = 1;         % Tolerance for height error
    err_pos_norm_tol = 0.7;  % Tolerance for (x, y) norm error

    clear ser;


    total_duration = 0;

    baud = 115200;
    ser = serialport(com_port, baud);
    pause(2);

    % Safety: Deflate all valves
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

        still_in_tolerance = false;
        iter = 0;

        while true
            iter = iter + 1;
            [~, pitch_new, roll_new, h_new] = read_sensors_filtered(ser, true);
            measured_pitch = pitch_new;
            measured_roll  = roll_new;
            measured_h     = h_new;

            [x_c, y_c, h_c] = prh_to_xyh(measured_pitch, measured_roll, measured_h);

            pos_error = [desired_x - x_c, desired_y - y_c, desired_h - h_c];
            pos_norm = norm(pos_error(1:2));
            h_error = pos_error(3);

            [hA_meas, hB_meas, hC_meas] = prh_to_leg_heights(measured_pitch, measured_roll, measured_h);

            fprintf('\n[Step %d]\n', iter);
            fprintf('Current Leg Heights:    [%.2f %.2f %.2f]\n', hA_meas, hB_meas, hC_meas);
            fprintf('Current PRH:            [%.2f %.2f %.2f]\n', measured_pitch, measured_roll, measured_h);
            fprintf('Current Position:       [%.2f %.2f %.2f]\n', x_c, y_c, h_c);
            fprintf('Position error:         [%.2f %.2f] (norm=%.2f)\n', pos_error(1), pos_error(2), pos_norm);
            fprintf('H error: [%.2f]\n', h_error);
            fprintf('Total_duration: [%.2f]\n',total_duration);

            if abs(pos_norm) < err_pos_norm_tol && abs(h_error) < err_h_tol
                if ~still_in_tolerance
                    disp('In Tolerance');
                    still_in_tolerance = true;
                end
                pause(0.3); 
                continue
            else
                still_in_tolerance = false;
                disp('Out of Tolerance');

                for k = 1:max_iter
                    [hA_meas, hB_meas, hC_meas] = prh_to_leg_heights(measured_pitch, measured_roll, measured_h);

                    err_A = hA_des - hA_meas;
                    err_B = hB_des - hB_meas;
                    err_C = hC_des - hC_meas;

                    tA = Kp * err_A;
                    tB = Kp * err_B;
                    tC = Kp * err_C;

                    write_one_valve_millis(ser, 1, tC);
                    write_one_valve_millis(ser, 2, tA);
                    write_one_valve_millis(ser, 3, tB);

                    pause_duration = max([100, abs(tA), abs(tB), abs(tC)]+10) / 1000;
                    total_duration = total_duration + pause_duration;
                    pause(pause_duration);

                    [~, pitch_new, roll_new, h_new] = read_sensors_filtered(ser, true);
                    measured_pitch = pitch_new;
                    measured_roll  = roll_new;
                    measured_h     = h_new;

                    [x_c, y_c, h_c] = prh_to_xyh(measured_pitch, measured_roll, measured_h);
                    pos_error = [desired_x - x_c, desired_y - y_c, desired_h - h_c];
                        pos_norm = norm(pos_error(1:2));
                    h_error = pos_error(3);

                    fprintf('\n[CONTROL Step %d]\n', k);
                    fprintf('Valve times (ms):       [%.2f %.2f %.2f]\n', tA, tB, tC);
                    fprintf('Desired Leg Heights:    [%.2f %.2f %.2f]\n', hA_des, hB_des, hC_des);
                    fprintf('Current Leg Heights:    [%.2f %.2f %.2f]\n', hA_meas, hB_meas, hC_meas);
                    fprintf('Desired PRH:            [%.2f %.2f %.2f]\n', desired_pitch, desired_roll, desired_h);
                    fprintf('Current PRH:            [%.2f %.2f %.2f]\n', measured_pitch, measured_roll, measured_h);
                    fprintf('Current Position:       [%.2f %.2f %.2f]\n', x_c, y_c, h_c);
                    fprintf('Position error:         [%.2f %.2f] (norm=%.2f)\n', pos_error(1), pos_error(2), pos_norm);
                    fprintf('H error: [%.2f]\n', h_error);
                    fprintf('Total_duration: [%.2f]\n',total_duration);

                    if abs(pos_norm) < err_pos_norm_tol && abs(h_error) < err_h_tol
                        disp('Tolerance bandına tekrar girildi.');
                        iter = 0;
                        total_duration=0;
                        break
                    end
                end
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
end
