function [pitch_final_deg, roll_final_deg, h_final] = xyh_to_prh(desired_x, desired_y, desired_h)
    % Finds the pitch, roll, and h that achieve the given (x, y, h) center
    % Inputs:
    %   desired_x: Target X coordinate of center (mm)
    %   desired_y: Target Y coordinate of center (mm)
    %   desired_h: Target height (mm)
    % Outputs:
    %   pitch_final_deg: Pitch angle in degrees
    %   roll_final_deg:  Roll angle in degrees
    %   h_final:         Height (mm)

    x0 = [0, 0, desired_h];
    options = optimset('Display','off');
    
    % rotation matrix 
    rotation_matrix = @(pitch, roll) ...
        [ cos(pitch), sin(roll)*sin(pitch),  -cos(roll)*sin(pitch);
          0,          cos(roll),             sin(roll);
          sin(pitch), -sin(roll)*cos(pitch), cos(roll)*cos(pitch) ];

    % minimize the error between current and desired center
    sol = fminsearch(@(x) desired_midpoint(x, desired_x, desired_y, desired_h, rotation_matrix), x0, options);

    pitch_final_deg = sol(1);
    roll_final_deg  = sol(2);
    h_final         = sol(3);
end

function err = desired_midpoint(x, desired_x, desired_y, desired_h, rotation_matrix)
    % Cost function to minimize the distance
    pitch_deg = x(1);
    roll_deg  = x(2);
    h         = x(3);

    pitch = deg2rad(pitch_deg);
    roll  = deg2rad(roll_deg);

    % Calculate normal vector after rotation
    n = [0; 0; 1];
    R = rotation_matrix(pitch, roll);
    normal = R * n;
    normal = normal / norm(normal);

    % Calculate center position from normal and h
    cx = h * normal(2); % x = normal(2)
    cy = h * normal(1); % y = normal(1)
    cz = h * normal(3); % z = normal(3)

    % Squared error
    err = (desired_x - cx)^2 + (desired_y - cy)^2 + (desired_h - cz)^2;
end
