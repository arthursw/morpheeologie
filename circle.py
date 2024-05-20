import math

radius = 20
n_drops = 20
pos_z_up = 100
pos_z_down = 100
inject_min = -10
inject_max = -10
inject_amount = -10
speed_min = 8000
speed_max = 8000
speed = 8000
skip_up = True
both = False

center_x = 150
center_y = 80

n_circles = 1
plane_pause = 0 #in ms

# Home
# Center of printer: X150 Y80
# Good Z for jar : X110     G0 Z105
# Initialize injection : G0 E-1000
# commands = ['G90', 'M83', 'G28 X Y', 'G0 F8000 X150 Y80', 'G0 F8000']
commands = ['G90', 'M83', 'G0 F8000']

commands.append(f'G0 X{center_x} Y{center_y}')

for n in range(n_circles):
    total = float(n_circles-1 if n_circles>1 else 1)
    inject_amount = inject_min + (n / total) * (inject_max - inject_min)
    speed = speed_min + (n / total) * (speed_max - speed_min)
    commands.append(f'G0 F{speed:.2f}')
    for i in range(n_drops):
        angle = (2*math.pi*i)/float(n_drops)
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        if both:
            commands.append(f'G0 X{x:.2f} Y{y:.2f} E{inject_amount}')
        else: 
            # go to position
            commands.append(f'G0 X{x:.2f} Y{y:.2f}')
            if not skip_up:
                # up
                commands.append(f'G0 Z{pos_z_down}')
            # inject
            commands.append(f'G0 E{inject_amount}')
            if not skip_up:
                # down
                commands.append(f'G0 Z{pos_z_up}')
    # pause 
    commands.append(f'G4 P{plane_pause}')

commands.append(f'G0 X{center_x} Y{center_y}')

with open('circle.gcode', 'w') as f:
    for command in commands:
        f.write(command+'\n')

# 30 / 30 = 0.5 / 0.5
# 30 / 90 = 0.25 / 0.75