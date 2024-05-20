include <BOSL2/std.scad>

thickness = 3;
width = 22;
length = 89;
screw_distance = 79;
niddle_diameter = 6;
niddle_holder_height = 2;
niddle_case_outer_diameter = 10.5;
niddle_holder_height_2 = 12;
niddle_case_outer_thickness = 1;

$fs = 0.1;

module plate() {
    difference() {
        cube([width,length,thickness], center=true);

        yflip_copy(offset=screw_distance/2) {
            cylinder(d=3, h=10, center=true);
        }
        cylinder(d=niddle_diameter, h=10, center=true);
    }
}
module print() {
    up(niddle_holder_height/2+thickness/2)
    tube(h=niddle_holder_height, od=niddle_diameter+1, id=niddle_diameter);

    up(niddle_holder_height_2/2+thickness/2)
    tube(h=niddle_holder_height_2, od=niddle_case_outer_diameter+2*niddle_case_outer_thickness, id=niddle_case_outer_diameter);

    plate();
}

// projection() print();
// plate();
print();