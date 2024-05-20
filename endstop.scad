include <BOSL2/std.scad>

$fs = 0.1;

thickness = 3;
strut_height = 5;
width = 22;
length = 10;
screw_diameter = 3;
strut_diameter = 5;

head_height = 30;
head_width = 7;

head_top_height = 20;
head_top_width = 10;
head_top_z = head_height-head_top_height;

wedge_width = thickness;//head_width;
wedge_height = 30;
wedge_length = length - thickness;

module head() {

    left(wedge_width/2)
    wedge([wedge_width, wedge_length, wedge_height]);

    up(head_height/2)
    cube([head_width,thickness,head_height], center=true);
    up(head_height/2+head_top_z/2)
    right(head_width/2+head_top_width/2)
    cube([head_top_width,thickness,head_top_height], center=true);
}

union() {
    difference() {
        union() {
            up(thickness/2)
            cube([width,length,thickness], center=true);
            cylinder(d=strut_diameter, h=strut_height);
        }
        down(0.1)
        cylinder(d=screw_diameter, h=strut_height+1);
    }

    translate([width/2-head_width/2,-length/2+thickness/2,thickness])
    head();
}