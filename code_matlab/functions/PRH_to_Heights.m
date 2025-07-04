

%Constants
L = 170;
h_center = 60;

% Example Values
pitch_deg = 0;
roll_deg  = 0;  
h_new     = 68;

% Initial triangle (center at origin)
h_tri = sqrt(3)/2 * L;
A0 = [-L/2, -h_tri/3, h_center];
B0 = [ L/2, -h_tri/3, h_center];
C0 = [   0 , 2*h_tri/3, h_center];
center0 = mean([A0; B0; C0],1);

% Pitch/roll to normal vector
pitch = deg2rad(pitch_deg);
roll  = deg2rad(roll_deg);

rotation_matrix = [ ...
    cos(pitch), sin(roll)*sin(pitch),  -cos(roll)*sin(pitch)
    0,          cos(roll),              sin(roll)
    sin(pitch), -sin(roll)*cos(pitch), cos(roll)*cos(pitch) ];

n = rotation_matrix * [0;0;1];
n = n / norm(n);

center_new = h_new * n';

A0c = A0 - center0;
B0c = B0 - center0;
C0c = C0 - center0;

old_normal = [0;0;1];
new_normal = n;

if norm(cross(old_normal,new_normal)) < 1e-8
    R_align = eye(3);
else
    v = cross(old_normal, new_normal);

    k = v / norm(v);

    K = [0 -k(3) k(2); k(3) 0 -k(1); -k(2) k(1) 0]; %skew symmetric

    theta = atan2(norm(v), dot(old_normal, new_normal)); %rotation angle

    R_align = eye(3) + sin(theta)*K + (1-cos(theta))*K^2; % Rodrigues' rotation formula in matrix

end

A1 = center_new + (R_align * A0c')';
B1 = center_new + (R_align * B0c')';
C1 = center_new + (R_align * C0c')';



len_AB = norm(A1 - B1);
len_BC = norm(B1 - C1);
len_CA = norm(C1 - A1);


fprintf('=== NEW CENTER ===\n');
fprintf('x = %.2f mm, y = %.2f mm, z = %.2f mm\n', center_new);
fprintf('\n=== NEW CORNERS ===\n');
fprintf('A: [%.2f, %.2f, %.2f]\n', A1);
fprintf('B: [%.2f, %.2f, %.2f]\n', B1);
fprintf('C: [%.2f, %.2f, %.2f]\n', C1);

fprintf('\n--- Side Lengths (should stay near %.2f mm) ---\n', L);
fprintf('AB: %.2f mm\n', len_AB);
fprintf('BC: %.2f mm\n', len_BC);
fprintf('CA: %.2f mm\n', len_CA);

figure; hold on; grid on; axis equal;

fill3([A0(1), B0(1), C0(1)], [A0(2), B0(2), C0(2)], [A0(3), B0(3), C0(3)], ...
    'b', 'FaceAlpha',0.15, 'EdgeColor','b', 'LineWidth',2);

fill3([A1(1), B1(1), C1(1)], [A1(2), B1(2), C1(2)], [A1(3), B1(3), C1(3)], ...
    'r', 'FaceAlpha',0.20, 'EdgeColor','r', 'LineWidth',2);

plot3(A0(1), A0(2), A0(3), 'bo', 'MarkerSize',10, 'MarkerFaceColor','b');
plot3(B0(1), B0(2), B0(3), 'bo', 'MarkerSize',10, 'MarkerFaceColor','b');
plot3(C0(1), C0(2), C0(3), 'bo', 'MarkerSize',10, 'MarkerFaceColor','b');
plot3(center0(1), center0(2), center0(3), 'bx', 'MarkerSize',14, 'LineWidth',2);

plot3(A1(1), A1(2), A1(3), 'ro', 'MarkerSize',10, 'MarkerFaceColor','r');
plot3(B1(1), B1(2), B1(3), 'ro', 'MarkerSize',10, 'MarkerFaceColor','r');
plot3(C1(1), C1(2), C1(3), 'ro', 'MarkerSize',10, 'MarkerFaceColor','r');
plot3(center_new(1), center_new(2), center_new(3), 'gx', 'MarkerSize',14, 'LineWidth',2);

text(A0(1),A0(2),A0(3),'A_0','FontSize',12,'FontWeight','bold','Color','b');
text(B0(1),B0(2),B0(3),'B_0','FontSize',12,'FontWeight','bold','Color','b');
text(C0(1),C0(2),C0(3),'C_0','FontSize',12,'FontWeight','bold','Color','b');
text(center0(1),center0(2),center0(3),'C_0','FontSize',12,'FontWeight','bold','Color','b');
text(A1(1),A1(2),A1(3),'A_1','FontSize',12,'FontWeight','bold','Color','r');
text(B1(1),B1(2),B1(3),'B_1','FontSize',12,'FontWeight','bold','Color','r');
text(C1(1),C1(2),C1(3),'C_1','FontSize',12,'FontWeight','bold','Color','r');
text(center_new(1),center_new(2),center_new(3),'C_1','FontSize',12,'FontWeight','bold','Color','g');

xlabel('X (mm)'); ylabel('Y (mm)'); zlabel('Height (mm)');
title('Initial and Final Triangle (Pitch/Roll/h-based Rotation)');
view(3);
hold off;
