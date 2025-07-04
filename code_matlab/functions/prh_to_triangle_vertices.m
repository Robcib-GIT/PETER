function [A, B, C] = prh_to_triangle_vertices(pitch, roll, h, L)
    h_tri = sqrt(3)/2 * L;
    A0 = [-L/2, -h_tri/3, h];
    B0 = [ L/2, -h_tri/3, h];
    C0 = [   0 , 2*h_tri/3, h];
    pitch_rad = deg2rad(pitch);
    roll_rad  = deg2rad(roll);
    R = [cos(pitch_rad) sin(roll_rad)*sin(pitch_rad) -cos(roll_rad)*sin(pitch_rad); ...
         0              cos(roll_rad)               sin(roll_rad); ...
         sin(pitch_rad) -sin(roll_rad)*cos(pitch_rad) cos(roll_rad)*cos(pitch_rad)];
    n = R*[0;0;1];
    n = n / norm(n);
    center = h * n;
    center0 = mean([A0; B0; C0],1);
    A = center' + (A0 - center0);
    B = center' + (B0 - center0);
    C = center' + (C0 - center0);
end
