function [hA, hB, hC] = prh_to_leg_heights(pitch_deg, roll_deg, h_new)
    % Calculates new leg heights (hA, hB, hC) from pitch, roll and h
    % Inputs:
    %   pitch_deg: Pitch angle in degrees
    %   roll_deg: Roll angle in degrees
    %   h_new:     Desired center height (mm)
    % Outputs:
    %   hA, hB, hC: Leg heights (mm)
    
    % System constants
    L = 170;
    h_center = 60;
    
    % Initial triangle (centered at origin)
    h_tri = sqrt(3)/2 * L;
    A0 = [-L/2, -h_tri/3, h_center];
    B0 = [ L/2, -h_tri/3, h_center];
    C0 = [   0 , 2*h_tri/3, h_center];
    center0 = mean([A0; B0; C0], 1);

    % Convert input angles to radians
    pitch = deg2rad(pitch_deg);
    roll  = deg2rad(roll_deg);

    % Rotation matrix from pitch and roll
    rotation_matrix = [ ...
        cos(pitch),  sin(roll)*sin(pitch),   -cos(roll)*sin(pitch);
        0,           cos(roll),              sin(roll);
        sin(pitch), -sin(roll)*cos(pitch),   cos(roll)*cos(pitch)];
    
    % New normal vector after pitch/roll
    n = rotation_matrix * [0;0;1];
    n = n / norm(n);

    % New triangle center in 3D space
    center_new = h_new * n';

    % Find old corner vectors relative to the center
    A0c = A0 - center0;
    B0c = B0 - center0;
    C0c = C0 - center0;

    old_normal = [0;0;1];
    new_normal = n;

    % Find rotation matrix to align old normal to new normal
    if norm(cross(old_normal, new_normal)) < 1e-8
        R_align = eye(3);
    else
        v = cross(old_normal, new_normal);
        k = v / norm(v);
        K = [0 -k(3) k(2); k(3) 0 -k(1); -k(2) k(1) 0]; % Skew-symmetric
        theta = atan2(norm(v), dot(old_normal, new_normal)); % Angle
        R_align = eye(3) + sin(theta)*K + (1-cos(theta))*K^2; % Rodrigues' formula
    end

    % Calculate new corner positions in 3D
    A1 = center_new + (R_align * A0c')';
    B1 = center_new + (R_align * B0c')';
    C1 = center_new + (R_align * C0c')';

    % Leg heights are the Z components (distance from ground)
    hA = A1(3);
    hB = B1(3);
    hC = C1(3);
end
