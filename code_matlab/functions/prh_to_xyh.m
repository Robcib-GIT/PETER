function [x, y, h_out] = prh_to_xyh(pitch_deg, roll_deg, h)
    % Calculates the (x, y, h) position of the platform center
    % Inputs:
    %   pitch_deg: Pitch angle in degrees (from IMU)
    %   roll_deg:  Roll angle in degrees (from IMU)
    %   h:         Height from TOF sensor (mm)
    % Outputs:
    %   x:         X coordinate of center (mm)
    %   y:         Y coordinate of center (mm)
    %   h_out:     Height (same as input h)
    
    % Convert input angles from degrees to radians
    pitch = deg2rad(pitch_deg);
    roll  = deg2rad(roll_deg);

    % Define the rotation matrix as in the original script
    R = [ cos(pitch), sin(roll)*sin(pitch),  -cos(roll)*sin(pitch);
          0,          cos(roll),              sin(roll);
          sin(pitch), -sin(roll)*cos(pitch),  cos(roll)*cos(pitch) ];

    % Initial normal vector (platform points upwards)
    n = [0; 0; 1];

    % Apply the rotation to the normal vector
    normal = R * n;

    % Normalize the normal vector (just in case)
    normal = normal / norm(normal);

    % Swap and scale as per original script
    % x = normal(2), y = normal(1), z = normal(3)
    x = h * normal(2);
    y = h * normal(1);
    h_out = h*normal(3); % Return the same height

end
