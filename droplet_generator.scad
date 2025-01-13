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

module niddle_holder() {
    up(niddle_holder_height/2+thickness/2)
    tube(h=niddle_holder_height, od=niddle_diameter+1, id=niddle_diameter);

    up(niddle_holder_height_2/2+thickness/2)
    tube(h=niddle_holder_height_2, od=niddle_case_outer_diameter+2*niddle_case_outer_thickness, id=niddle_case_outer_diameter);

    plate();
}

niddle_base_height = 12;
niddle_base_head_height = 1;

module niddle_base() {
    difference() {
        union() {
            // Head
            recolor("lightblue")
            up(niddle_base_height-niddle_base_head_height)
            union() {
                cylinder(h=niddle_base_head_height, d=6.5);
                up(niddle_base_head_height/2)
                cube([7.5,4,niddle_base_head_height], center=true);
            }

            // Body
            cylinder(h=niddle_base_height, d1=4, d2=5.5);
            up(niddle_base_height/2)
            cylinder(h=niddle_base_height/2, d=5.5);
        }
        down(0.5)
        cylinder(h=niddle_base_height+1, d1=2, d2=4.5);
    }
}

press_thickness_top = 5;

module press_top() {
    up(7)
    up(press_thickness_top/2)
    // union() {
    difference() {
        cube([7.5,30,press_thickness_top], center=true);
        
        yflip_copy(offset=6)
        xrot(90)
        cylinder(h=8, d=2, center=true);

        up(1)
        yflip_copy(offset=10)
        cylinder(h=4, d=2, center=true);

        up(-1)
        yflip_copy(offset=2)
        cylinder(h=4, d=2, center=true);

        // notches
        up(-2.1)
        xflip_copy(offset=2.5)
        cylinder(h=1, d=1.5, center=true);
    }
}

press_thickness_bottom = 5;

module press_bottom() {
    // union() {
    difference() {
        union() {
            intersection() {
                cylinder(h=press_thickness_bottom, d=niddle_case_outer_diameter-0.5, center=true);
                cube([7.5,10,press_thickness_bottom], center=true);
            }

            // top notches
            up(press_thickness_bottom/2+0.45)
            xflip_copy(offset=2.5)
            cylinder(h=1, d=1.5, center=true);


            // bottom notch
            up(-press_thickness_bottom/2-3/2)
            cylinder(h=3, d=7, center=true);
        }
        
        up(1.8)
        yflip_copy(offset=2)
        cylinder(h=2, d=2, center=true);
        
        up(0.2)
        // yflip_copy(offset=-1.1)
        fwd(1.0)
        xrot(45)
        cylinder(h=3.5, d=2, center=true);
        
        up(1.3)
        fwd(-1.1)
        xrot(-45)
        cylinder(h=3.25, d=1, center=true);

        up(-3.25)
        cylinder(h=6, d=2, center=true);

        // bottom notch
        up(-4.01)
        cylinder(h=3, d=4, center=true);

    }

}

module niddle() {
    niddle_length = 50;
    down(2)
    union() {
        down(niddle_length/2)
        tube(h=niddle_length, od=3, id=2);
        
        // notch
        down(3/2)
        tube(h=3, od=4, id=2);
    }
}

module niddle_base_notch() {
    union() {
        niddle_base();
        
        // notch
        down(3/2)
        tube(h=3, od=4, id=2);
    }
}

module droplet_generator() {

    up(13)
    yflip_copy(offset=10)
    // left(10)
    niddle_base();

    // press top
    up(1)
    press_top();

    up(5.5)
    press_bottom();

    fwd(5)
    niddle();

    down(2)
    zflip()
    niddle_base_notch();
}

module print() {
    // #niddle_holder();

    up(6)
    droplet_generator();

}

print();