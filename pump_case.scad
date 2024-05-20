include <BOSL2/std.scad>
include <axe_link.scad>
include <BOSL2/nema_steppers.scad>


nema_side = 60;
thickness = 3;
pump_to_motor = cyl_length + 24-15;//30;
$fs = 0.1;
notch_size = 4*3;
epsilon=0.01;
screw_holder_size = 6;
m3d = 3;

module nema_holder() {
    difference() {
        cube([nema_side,nema_side,thickness], center=true);
        zrot(45)
        nema_mount_mask(size=17, depth=5, l=0);

        yflip_copy(offset=nema_side/2-thickness/2+epsilon)
        cube([nema_side-2*notch_size, thickness,10], center=true);

        xflip_copy(offset=nema_side/2-notch_size/2+epsilon)
        yflip_copy(offset=nema_side/2-thickness-screw_holder_size/2+epsilon)
        cyl(d=m3d, h=10);
    }
}

module pump_holder() {
    difference() {
        nema_holder();

        zrot(45) {
            xflip_copy(offset=48/2) {
                cylinder(d=m3d, h=10, center=true);
            }
            yflip_copy(offset=44/2) {
                cylinder(d=m3d, h=10, center=true);
            }
        }

        zrot_copies(n=4)
        translate([44/2,0,0])
        cylinder(d=7, h=10, center=true);
    }
}

module link_core() {
    difference() {
        cube([nema_side,pump_to_motor, thickness], center=true);

        xflip_copy(offset=nema_side/2-notch_size/2+epsilon)
        yflip_copy(offset=pump_to_motor/2-thickness/2+epsilon)
        cube([notch_size, thickness,10], center=true);
    }
}

module link() {
    union() {
        link_core();
        up(screw_holder_size/2+thickness/2)
        xflip_copy(offset=nema_side/2-notch_size/2+epsilon)
        yflip_copy(offset=pump_to_motor/2-1.5*thickness+epsilon)
        difference() {
            cube([notch_size, thickness, screw_holder_size], center=true);
            xrot(90)
            cylinder(d=m3d, h=10, center=true);
        }
    }
}

module laser_cut_link() {
    difference() {
        link_core();
    }
}

module assembly() {
    
    nema_holder();

    translate([0, 0, pump_to_motor/2-thickness/2])
    yflip_copy(offset=nema_side/2-thickness/2)
    xrot(90)
    link();
    translate([0, 0, pump_to_motor-thickness]) {
        pump_holder();
    }
    down(thickness/2)
    {
        // cylinder(d=5, h=24);
        up(24-15)
        axe_link();
    }
}

module print() {

    nema_holder();

    translate([nema_side/2, nema_side/2 + pump_to_motor/2 + 3, 0]) {
        xcopies(nema_side+3)
        link();
    }

    translate([nema_side+3, 0, 0]) {
        pump_holder();
    }   
}

module laser_cut() {

    nema_holder();

    translate([nema_side/2, nema_side/2 + pump_to_motor/2 + 3, 0]) {
        xcopies(nema_side+3)
        laser_cut_link();
    }

    translate([nema_side+3, 0, 0]) {
        pump_holder();
    }   
}

nema_side2 = 55;
module v2() {
    difference() {
        cube([nema_side2,nema_side2,thickness], center=true);
        // zrot(45)

        zrot(45) {
            nema_mount_mask(size=17, depth=5, l=0);
            xflip_copy(offset=48/2) {
                cylinder(d=m3d, h=10, center=true);
            }
            yflip_copy(offset=44/2) {
                cylinder(d=m3d, h=10, center=true);
            }
        }
    }
}
v2();
// print();
// assembly();
// laser_cut();
