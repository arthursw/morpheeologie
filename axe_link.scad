include <BOSL2/std.scad>
include <BOSL2/nema_steppers.scad>
$fs = 0.1;
    // MOTOR_WIDTH: The full width and length of the motor.
    // PLINTH_HEIGHT: The height of the circular plinth on the face of the motor.
    // PLINTH_DIAM: The diameter of the circular plinth on the face of the motor.
    // SCREW_SPACING: The spacing between screwhole centers in both X and Y axes.
    // SCREW_SIZE: The diameter of the screws.
    // SCREW_DEPTH: The depth of the screwholes.
    // SHAFT_DIAM: The diameter of the motor shaft.

// MOTOR_WIDTH, PLINTH_HEIGHT, PLINTH_DIAM, SCREW_SPACING, SCREW_SIZE, SCREW_DEPTH, SHAFT_DIAM = nema_motor_info(17);
info = nema_motor_info(17);
echo(info[6]);

shaft_diameter = info[6];
cyl_diameter = 10;
nema_axe_length = 15;
screw_diameter = 2;
screw_length = 4;
cyl_length = nema_axe_length + screw_length;

module nema_shaft() {

    difference() {
        cylinder(h=nema_axe_length, d=shaft_diameter);
        // fwd(shaft_diameter/2)
        translate([shaft_diameter/2-0.5, -shaft_diameter/2, 0])
        cube([0.5, shaft_diameter, nema_axe_length]);
    }
}
module axe_link() {
    difference() {
        cylinder(h=cyl_length, d=cyl_diameter);
        cylinder(h=cyl_length+0.1, d=screw_diameter);
        down(0.1)
        nema_shaft();
        cyl(d1);

        up(2-0.1)
        cyl(d1=shaft_diameter+2, d2=shaft_diameter-2, h=4);
    }
}

// axe_link();
// nema_shaft();